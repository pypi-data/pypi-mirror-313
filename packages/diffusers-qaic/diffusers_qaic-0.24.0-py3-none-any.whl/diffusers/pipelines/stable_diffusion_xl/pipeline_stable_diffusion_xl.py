import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import os
import time
from concurrent.futures import ThreadPoolExecutor, wait
import onnx
import qaic
import numpy as np
import torch
from transformers import (
    CLIPImageProcessor,
    CLIPTextModel,
    CLIPTextModelWithProjection,
    CLIPTokenizer,
    CLIPVisionModelWithProjection,
)

from ...image_processor import PipelineImageInput, VaeImageProcessor
from ...loaders import (
    FromSingleFileMixin,
    IPAdapterMixin,
    StableDiffusionXLLoraLoaderMixin,
    TextualInversionLoaderMixin,
)
from ...models import AutoencoderKL, UNet2DConditionModel
from ...models.attention_processor import (
    AttnProcessor2_0,
    LoRAAttnProcessor2_0,
    LoRAXFormersAttnProcessor,
    XFormersAttnProcessor,
)
from ...models.lora import adjust_lora_scale_text_encoder
from ...schedulers import KarrasDiffusionSchedulers
from ...utils import (
    USE_PEFT_BACKEND,
    deprecate,
    is_invisible_watermark_available,
    is_torch_xla_available,
    logging,
    replace_example_docstring,
    scale_lora_layers,
    unscale_lora_layers,
)
from ...utils.torch_utils import randn_tensor
from ..pipeline_utils import DiffusionPipeline
from .pipeline_output import StableDiffusionXLPipelineOutput


if is_invisible_watermark_available():
    from .watermark import StableDiffusionXLWatermarker

if is_torch_xla_available():
    import torch_xla.core.xla_model as xm

    XLA_AVAILABLE = True
else:
    XLA_AVAILABLE = False


logger = logging.get_logger(__name__)  # pylint: disable=invalid-name

EXAMPLE_DOC_STRING = """
    Examples:
        ```py
        >>> import torch
        >>> from diffusers import StableDiffusionXLPipeline

        >>> pipe = StableDiffusionXLPipeline.from_pretrained(
        ...     "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
        ... )
        >>> pipe = pipe.to("cuda")

        >>> prompt = "a photo of an astronaut riding a horse on mars"
        >>> image = pipe(prompt).images[0]
        ```
"""

def sample_from_quad_center(total_numbers, n_samples, center, pow=1.2):
    while pow > 1:
        # Generate linearly spaced values between 0 and a max value
        x_values = np.linspace((-center)**(1/pow), (total_numbers-center)**(1/pow), n_samples+1)
        indices = [0] + [x+center for x in np.unique(np.int32(x_values**pow))[1:-1]]
        if len(indices) == n_samples:
            break
        pow -=0.02
    if pow <= 1:
        raise ValueError("Cannot find suitable pow. Please adjust n_samples or decrease center.")
    return indices, pow

# Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.rescale_noise_cfg
def rescale_noise_cfg(noise_cfg, noise_pred_text, guidance_rescale=0.0):
    """
    Rescale `noise_cfg` according to `guidance_rescale`. Based on findings of [Common Diffusion Noise Schedules and
    Sample Steps are Flawed](https://arxiv.org/pdf/2305.08891.pdf). See Section 3.4
    """
    std_text = noise_pred_text.std(
        dim=list(range(1, noise_pred_text.ndim)), keepdim=True
    )
    std_cfg = noise_cfg.std(dim=list(range(1, noise_cfg.ndim)), keepdim=True)
    # rescale the results from guidance (fixes overexposure)
    noise_pred_rescaled = noise_cfg * (std_text / std_cfg)
    # mix with the original results from guidance by factor guidance_rescale to avoid "plain looking" images
    noise_cfg = (
        guidance_rescale * noise_pred_rescaled + (1 - guidance_rescale) * noise_cfg
    )
    return noise_cfg


# Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.retrieve_timesteps
def retrieve_timesteps(
    scheduler,
    num_inference_steps: Optional[int] = None,
    device: Optional[Union[str, torch.device]] = None,
    timesteps: Optional[List[int]] = None,
    **kwargs,
):
    """
    Calls the scheduler's `set_timesteps` method and retrieves timesteps from the scheduler after the call. Handles
    custom timesteps. Any kwargs will be supplied to `scheduler.set_timesteps`.

    Args:
        scheduler (`SchedulerMixin`):
            The scheduler to get timesteps from.
        num_inference_steps (`int`):
            The number of diffusion steps used when generating samples with a pre-trained model. If used,
            `timesteps` must be `None`.
        device (`str` or `torch.device`, *optional*):
            The device to which the timesteps should be moved to. If `None`, the timesteps are not moved.
        timesteps (`List[int]`, *optional*):
                Custom timesteps used to support arbitrary spacing between timesteps. If `None`, then the default
                timestep spacing strategy of the scheduler is used. If `timesteps` is passed, `num_inference_steps`
                must be `None`.

    Returns:
        `Tuple[torch.Tensor, int]`: A tuple where the first element is the timestep schedule from the scheduler and the
        second element is the number of inference steps.
    """
    if timesteps is not None:
        accepts_timesteps = "timesteps" in set(
            inspect.signature(scheduler.set_timesteps).parameters.keys()
        )
        if not accepts_timesteps:
            raise ValueError(
                f"The current scheduler class {scheduler.__class__}'s `set_timesteps` does not support custom"
                f" timestep schedules. Please check whether you are using the correct scheduler."
            )
        scheduler.set_timesteps(timesteps=timesteps, device=device, **kwargs)
        timesteps = scheduler.timesteps
        num_inference_steps = len(timesteps)
    else:
        scheduler.set_timesteps(num_inference_steps, device=device, **kwargs)
        timesteps = scheduler.timesteps
    return timesteps, num_inference_steps


class CustomDiffusionPipeline(DiffusionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _initialize_sessions(
        self,
        vae_decoder_qpc,
        unet_sess,
        unet_sess2,
        vae_decoder_sess,
        text_encoder_sess,
        text_encoder_2_sess,
        config_dict,
    ):
        self.vae_config = config_dict["vae"]
        self.text_encoder_config = config_dict["text_encoder"]
        self.text_encoder_2_config = config_dict["text_encoder_2"]
        self.unet_config = config_dict["unet"]
        # TODO: if unet_sess is (a,b), we should extract two things
        # deepcache supports or should we just replace unet_sess with small and big everytime it requires as it is just a pointer?
        # if isinstance(unet_sess, tuple):
        #     self.unet_sess = unet_sess[0]
        # else:
        self.unet_sess = unet_sess
        self.unet_sess2 = unet_sess2
        self.vae_decoder_qpc = vae_decoder_qpc
        self.vae_decoder_sess = vae_decoder_sess
        self.text_encoder_sess = text_encoder_sess
        self.text_encoder_2_sess = text_encoder_2_sess

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        # Custom logic to initialize components with QAIC sessions directly
        vae_decoder_qpc = kwargs.pop(
            "vae_decoder_qpc",
            "/home/krai/work_collection/model_sdxl_vae_decoder_with_block_size.64_scaling_factor.128_compiled_using_qaic_sdk_1.16.0.48_with_cores.16_mos.2_ols.1_batch_size.1/qpc/programqpc.bin",
        )
        text_encoder_qpc = kwargs.pop(
            "text_encoder_qpc",
            "/home/krai/work_collection/model_sdxl_text_encoder_compiled_using_qaic_sdk_1.16.0.48_with_cores.16/qpc/programqpc.bin",
        )
        text_encoder_2_qpc = kwargs.pop(
            "text_encoder_2_qpc",
            "/home/krai/work_collection/model_sdxl_text_encoder_2_compiled_using_qaic_sdk_1.16.0.48_with_cores.16/qpc/programqpc.bin",
        )
        unet_qpc = kwargs.pop(
            "unet_qpc",
            "/home/krai/work_collection/model_sdxl_unet_with_block_size.256_compiled_using_qaic_sdk_1.16.0.48_with_cores.16_mos.2_ols.1_batch_size.1/qpc/programqpc.bin",
        )
        vae_decoder_sess = kwargs.get("vae_decoder_sess", [None])
        text_encoder_sess = kwargs.get("text_encoder_sess", [None])
        text_encoder_2_sess = kwargs.get("text_encoder_2_sess", [None])
        unet_sess = kwargs.get("unet_sess", None)
        unet_sess2 = kwargs.get("unet_sess2", None)
        device_id = kwargs.get("device_id", 0)
        device_id2 = kwargs.get("device_id2", None)
        print(device_id, device_id2)

        from diffusers import DiffusionPipeline, EulerDiscreteScheduler

        print(pretrained_model_name_or_path)

        from transformers import AutoConfig
        import json

        # Load configurations directly from JSON files
        def load_config(subfolder):
            config_path = os.path.join(
                pretrained_model_name_or_path, subfolder, "config.json"
            )
            with open(config_path) as f:
                return json.load(f)

        vae_config = load_config("vae")
        text_encoder_config = load_config("text_encoder")
        text_encoder_2_config = load_config("text_encoder_2")
        unet_config = load_config("unet")

        # Load configurations without loading weights
        config_dict = {
            "vae": vae_config,  # AutoConfig.from_pretrained(pretrained_model_name_or_path, subfolder="vae", **kwargs),
            "text_encoder": text_encoder_config,  # AutoConfig.from_pretrained(pretrained_model_name_or_path, subfolder="text_encoder", **kwargs),
            "text_encoder_2": text_encoder_2_config,  # AutoConfig.from_pretrained(pretrained_model_name_or_path, subfolder="text_encoder_2", **kwargs),
            "unet": unet_config,  # AutoConfig.from_pretrained(pretrained_model_name_or_path, subfolder="unet", **kwargs)
        }
        # Initialize the model with components loaded onto the QAIC device
        components = {
            "tokenizer": CLIPTokenizer.from_pretrained(
                pretrained_model_name_or_path,
                subfolder="tokenizer",
                *model_args,
                **kwargs,
            ),
            "tokenizer_2": CLIPTokenizer.from_pretrained(
                pretrained_model_name_or_path,
                subfolder="tokenizer_2",
                *model_args,
                **kwargs,
            ),
            "scheduler": EulerDiscreteScheduler.from_pretrained(
                pretrained_model_name_or_path, subfolder="scheduler"
            ),
        }
        model = cls(**components)
        model._initialize_sessions(
            vae_decoder_qpc=vae_decoder_qpc,
            unet_sess=unet_sess,
            unet_sess2=unet_sess2,
            vae_decoder_sess=vae_decoder_sess,
            text_encoder_sess=text_encoder_sess,
            text_encoder_2_sess=text_encoder_2_sess,
            config_dict=config_dict,
        )
        return model


class StableDiffusionXLPipeline(
    CustomDiffusionPipeline,
    # FromSingleFileMixin,
    # StableDiffusionXLLoraLoaderMixin,
    # TextualInversionLoaderMixin,
    # IPAdapterMixin,
):
    r"""
    Pipeline for text-to-image generation using Stable Diffusion XL.

    This model inherits from [`DiffusionPipeline`]. Check the superclass documentation for the generic methods the
    library implements for all the pipelines (such as downloading or saving, running on a particular device, etc.)

    In addition the pipeline inherits the following loading methods:
        - *LoRA*: [`loaders.StableDiffusionXLLoraLoaderMixin.load_lora_weights`]
        - *Ckpt*: [`loaders.FromSingleFileMixin.from_single_file`]

    as well as the following saving methods:
        - *LoRA*: [`loaders.StableDiffusionXLLoraLoaderMixin.save_lora_weights`]

    Args:
        vae ([`AutoencoderKL`]):
            Variational Auto-Encoder (VAE) Model to encode and decode images to and from latent representations.
        text_encoder ([`CLIPTextModel`]):
            Frozen text-encoder. Stable Diffusion XL uses the text portion of
            [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTextModel), specifically
            the [clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14) variant.
        text_encoder_2 ([` CLIPTextModelWithProjection`]):
            Second frozen text-encoder. Stable Diffusion XL uses the text and pool portion of
            [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTextModelWithProjection),
            specifically the
            [laion/CLIP-ViT-bigG-14-laion2B-39B-b160k](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k)
            variant.
        tokenizer (`CLIPTokenizer`):
            Tokenizer of class
            [CLIPTokenizer](https://huggingface.co/docs/transformers/v4.21.0/en/model_doc/clip#transformers.CLIPTokenizer).
        tokenizer_2 (`CLIPTokenizer`):
            Second Tokenizer of class
            [CLIPTokenizer](https://huggingface.co/docs/transformers/v4.21.0/en/model_doc/clip#transformers.CLIPTokenizer).
        unet ([`UNet2DConditionModel`]): Conditional U-Net architecture to denoise the encoded image latents.
        scheduler ([`SchedulerMixin`]):
            A scheduler to be used in combination with `unet` to denoise the encoded image latents. Can be one of
            [`DDIMScheduler`], [`LMSDiscreteScheduler`], or [`PNDMScheduler`].
        force_zeros_for_empty_prompt (`bool`, *optional*, defaults to `"True"`):
            Whether the negative prompt embeddings shall be forced to always be set to 0. Also see the config of
            `stabilityai/stable-diffusion-xl-base-1-0`.
        add_watermarker (`bool`, *optional*):
            Whether to use the [invisible_watermark library](https://github.com/ShieldMnt/invisible-watermark/) to
            watermark output images. If not defined, it will default to True if the package is installed, otherwise no
            watermarker will be used.
    """

    model_cpu_offload_seq = "text_encoder->text_encoder_2->unet->vae"
    _optional_components = [
        "tokenizer",
        "tokenizer_2",
        "text_encoder",
        "text_encoder_2",
        "image_encoder",
        "feature_extractor",
    ]
    _callback_tensor_inputs = [
        "latents",
        "prompt_embeds",
        "negative_prompt_embeds",
        "add_text_embeds",
        "add_time_ids",
        "negative_pooled_prompt_embeds",
        "negative_add_time_ids",
    ]

    def __init__(
        self,
        # vae: AutoencoderKL,
        # text_encoder: CLIPTextModel,
        # text_encoder_2: CLIPTextModelWithProjection,
        tokenizer: CLIPTokenizer,
        tokenizer_2: CLIPTokenizer,
        # unet: UNet2DConditionModel,
        scheduler: KarrasDiffusionSchedulers,
        image_encoder: CLIPVisionModelWithProjection = None,
        feature_extractor: CLIPImageProcessor = None,
        force_zeros_for_empty_prompt: bool = True,
        add_watermarker: Optional[bool] = None,
        device_id: Optional[int] = 0,
        device_id2: Optional[int] = None,
        text_encoder_qpc: Optional[
            str
        ] = "./qpc/text_encoder-16c_1.14.0.14/programqpc.bin",
        text_encoder_2_qpc: Optional[
            str
        ] = "./qpc/text_encoder_2-16c_1.14.0.14/programqpc.bin",
        vae_decoder_qpc: Optional[
            str
        ] = "./qpc/vae_decoder_fixed128_dfs_1.14.0.14/programqpc.bin",
        unet_qpc: Optional[
            str
        ] = "./qpc/unet-bs2-mos2-ols1-16c_1.14.0.14/programqpc.bin",
        text_encoder_sess=None,
        text_encoder_2_sess=None,
        vae_decoder_sess=None,
        # <qaic.session._Session object at 0x7fb38467de20>
        unet_sess=None,
        unet_sess2=None,
        group_name: Optional[str] = "",
    ):
        super().__init__()
        print("-----------------------------------")
        print("----Pipeline init in stable diffusion XL pipeline")
        print(
            f"----text_encoder_sess before: {text_encoder_sess}, in stable diffusion XL pipeline"
        )
        print(
            f"----text_encoder_sess type: {type(text_encoder_sess)}, in stable diffusion XL pipeline"
        )
        if isinstance(text_encoder_sess, list):
            print(
                f"----text_encoder_sess length: {len(text_encoder_sess)}, in stable diffusion XL pipeline"
            )
            print(
                f"----text_encoder_sess[0]: {text_encoder_sess[0]}, in stable diffusion XL pipeline"
            )
        print("-----------------------------------")
        self.vae_decoder_sess = vae_decoder_sess
        self.text_encoder_sess = text_encoder_sess
        self.text_encoder_2_sess = text_encoder_2_sess
        self.unet_sess = unet_sess
        self.unet_sess2 = unet_sess2

        print(
            "----check sessions in stablediffusionXL pipeline:",
            self.text_encoder_sess,
            self.text_encoder_2_sess,
            self.vae_decoder_sess,
            self.unet_sess,
            self.unet_sess2,
        )

        if self.unet_sess2 is None:
            self.executor = ThreadPoolExecutor()

        self.register_modules(
            tokenizer=tokenizer,
            tokenizer_2=tokenizer_2,
            scheduler=scheduler,
        )
        self.register_to_config(
            force_zeros_for_empty_prompt=force_zeros_for_empty_prompt
        )
        # self.vae_scale_factor = 2 ** (len(self.vae_config.block_out_channels) - 1)
        # self.image_processor = VaeImageProcessor(vae_scale_factor=self.vae_scale_factor)
        self.vae_scale_factor = 2 * 4  # or any appropriate scale factor
        self.image_processor = VaeImageProcessor(vae_scale_factor=self.vae_scale_factor)
        self.default_sample_size = 128  # or any appropriate sample size
        self.expected_add_embed_dim = 2816  # or any appropriate dimension

        # self.default_sample_size = self.unet_config.sample_size
        self.group_name = group_name
        # del unet, vae, text_encoder, text_encoder_2

        add_watermarker = (
            add_watermarker
            if add_watermarker is not None
            else is_invisible_watermark_available()
        )

        if add_watermarker:
            self.watermark = StableDiffusionXLWatermarker()
        else:
            self.watermark = None

        self.guidance_scale = 8
        self.guidance_rescale = 8
        self.do_classifier_free_guidance = True
        self.interval_seq = None
        self.prv_features = None

    def enable_deepcache(self, interval_seq):
        """Enable DeepCache mode with given interval sequence"""
        self.interval_seq = interval_seq

    @property
    def num_timesteps(self):
        return self._num_timesteps

    @property
    def clip_skip(self):
        return self._clip_skip

    @property
    def cross_attention_kwargs(self):
        return self._cross_attention_kwargs

    @property
    def denoising_end(self):
        return self._denoising_end

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.enable_vae_slicing
    def enable_vae_slicing(self):
        r"""
        Enable sliced VAE decoding. When this option is enabled, the VAE will split the input tensor in slices to
        compute decoding in several steps. This is useful to save some memory and allow larger batch sizes.
        """
        self.vae.enable_slicing()

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.disable_vae_slicing
    def disable_vae_slicing(self):
        r"""
        Disable sliced VAE decoding. If `enable_vae_slicing` was previously enabled, this method will go back to
        computing decoding in one step.
        """
        self.vae.disable_slicing()

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.enable_vae_tiling
    def enable_vae_tiling(self):
        r"""
        Enable tiled VAE decoding. When this option is enabled, the VAE will split the input tensor into tiles to
        compute decoding and encoding in several steps. This is useful for saving a large amount of memory and to allow
        processing larger images.
        """
        self.vae.enable_tiling()

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.disable_vae_tiling
    def disable_vae_tiling(self):
        r"""
        Disable tiled VAE decoding. If `enable_vae_tiling` was previously enabled, this method will go back to
        computing decoding in one step.
        """
        self.vae.disable_tiling()

    # 20240703 PM
    def _encode_positive_prompt(
        self,
        prompt,
        prompt_2,
        tokenizer,
        tokenizer_2,
        text_encoder_sess,
        text_encoder_2_sess,
    ):
        prompt_embeds_1 = self._encode_prompt_sess1(
            prompt, tokenizer, text_encoder_sess
        )
        prompt_embeds_2, pooled_prompt_embeds = self._encode_prompt_sess2(
            prompt_2, tokenizer_2, text_encoder_2_sess
        )
        prompt_embeds = torch.cat([prompt_embeds_1, prompt_embeds_2], dim=-1)
        return prompt_embeds, pooled_prompt_embeds

    def _encode_negative_prompt(
        self,
        negative_prompt,
        negative_prompt_2,
        tokenizer,
        tokenizer_2,
        text_encoder_sess,
        text_encoder_2_sess,
    ):
        negative_prompt_embeds_1 = self._encode_prompt_sess1(
            negative_prompt, tokenizer, text_encoder_sess
        )
        (
            negative_prompt_embeds_2,
            negative_pooled_prompt_embeds,
        ) = self._encode_prompt_sess2(
            negative_prompt_2, tokenizer_2, text_encoder_2_sess
        )
        negative_prompt_embeds = torch.cat(
            [negative_prompt_embeds_1, negative_prompt_embeds_2], dim=-1
        )
        return negative_prompt_embeds, negative_pooled_prompt_embeds

    def _encode_prompt_sess1(self, prompt, tokenizer, text_encoder):
        if isinstance(self, TextualInversionLoaderMixin):
            prompt = self.maybe_convert_prompt(prompt, tokenizer)

        text_inputs = tokenizer(
            prompt,
            padding="max_length",
            max_length=tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        )

        text_input_ids = text_inputs.input_ids
        untruncated_ids = tokenizer(
            prompt, padding="longest", return_tensors="pt"
        ).input_ids

        if untruncated_ids.shape[-1] >= text_input_ids.shape[-1] and not torch.equal(
            text_input_ids, untruncated_ids
        ):
            removed_text = tokenizer.batch_decode(
                untruncated_ids[:, tokenizer.model_max_length - 1 : -1]
            )
            logger.warning(
                f"The following part of your input was truncated because CLIP can only handle sequences up to {tokenizer.model_max_length} tokens: {removed_text}"
            )

        inputname = "input_ids"
        print(type(text_encoder))
        i_shape, i_type = text_encoder.model_input_shape_dict[inputname]
        input_dict = {inputname: text_input_ids.numpy().astype(i_type)}
        output = text_encoder.run(input_dict)

        hidden_state_name = f"hidden_states.{11}"
        o_shape, o_type = text_encoder.model_output_shape_dict[hidden_state_name]
        embeds = torch.from_numpy(
            np.frombuffer(output[hidden_state_name], dtype=o_type).reshape(o_shape)
        )

        return embeds

    def _encode_prompt_sess2(self, prompt, tokenizer, text_encoder):
        if isinstance(self, TextualInversionLoaderMixin):
            prompt = self.maybe_convert_prompt(prompt, tokenizer)

        text_inputs = tokenizer(
            prompt,
            padding="max_length",
            max_length=tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        )

        text_input_ids = text_inputs.input_ids
        untruncated_ids = tokenizer(
            prompt, padding="longest", return_tensors="pt"
        ).input_ids

        if untruncated_ids.shape[-1] >= text_input_ids.shape[-1] and not torch.equal(
            text_input_ids, untruncated_ids
        ):
            removed_text = tokenizer.batch_decode(
                untruncated_ids[:, tokenizer.model_max_length - 1 : -1]
            )
            logger.warning(
                f"The following part of your input was truncated because CLIP can only handle sequences up to {tokenizer.model_max_length} tokens: {removed_text}"
            )

        inputname = "input_ids"
        i_shape, i_type = text_encoder.model_input_shape_dict[inputname]
        input_dict = {inputname: text_input_ids.numpy().astype(i_type)}
        output = text_encoder.run(input_dict)

        hidden_state_name = f"hidden_states.{31}"
        o_shape, o_type = text_encoder.model_output_shape_dict[hidden_state_name]
        embeds = torch.from_numpy(
            np.frombuffer(output[hidden_state_name], dtype=o_type).reshape(o_shape)
        )

        o_shape, o_type = text_encoder.model_output_shape_dict["text_embeds"]
        pooled_embeds = torch.from_numpy(
            np.frombuffer(output["text_embeds"], dtype=o_type).reshape(o_shape)
        )

        return embeds, pooled_embeds

    def encode_prompt(
        self,
        prompt: str,
        prompt_2: Optional[str] = None,
        device: Optional[torch.device] = None,
        num_images_per_prompt: int = 1,
        do_classifier_free_guidance: bool = True,
        negative_prompt: Optional[str] = None,
        negative_prompt_2: Optional[str] = None,
        prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_prompt_embeds: Optional[torch.FloatTensor] = None,
        pooled_prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_pooled_prompt_embeds: Optional[torch.FloatTensor] = None,
        lora_scale: Optional[float] = None,
        clip_skip: Optional[int] = None,
    ):
        device = device or self._execution_device

        # Handle LoRA scale
        if lora_scale is not None and isinstance(
            self, StableDiffusionXLLoraLoaderMixin
        ):
            self._lora_scale = lora_scale
            adjust_lora_scale_text_encoder(self.text_encoder, lora_scale)
            adjust_lora_scale_text_encoder(self.text_encoder_2, lora_scale)

        # Prepare prompts
        if prompt is not None:
            batch_size = len(prompt) if isinstance(prompt, list) else 1
        else:
            batch_size = prompt_embeds.shape[0]

        prompt = [prompt] if isinstance(prompt, str) else prompt
        prompt_2 = prompt_2 or prompt
        prompt_2 = [prompt_2] if isinstance(prompt_2, str) else prompt_2

        # Process positive prompt
        if prompt_embeds is None:
            prompt_embeds, pooled_prompt_embeds = self._encode_positive_prompt(
                prompt,
                prompt_2,
                self.tokenizer,
                self.tokenizer_2,
                self.text_encoder_sess,
                self.text_encoder_2_sess,
            )

        # Process negative prompt
        if do_classifier_free_guidance:
            if negative_prompt_embeds is None:
                if negative_prompt is None:
                    negative_prompt = [""] * batch_size
                negative_prompt = (
                    [negative_prompt]
                    if isinstance(negative_prompt, str)
                    else negative_prompt
                )
                negative_prompt_2 = negative_prompt_2 or negative_prompt
                negative_prompt_2 = (
                    [negative_prompt_2]
                    if isinstance(negative_prompt_2, str)
                    else negative_prompt_2
                )

                (
                    negative_prompt_embeds,
                    negative_pooled_prompt_embeds,
                ) = self._encode_negative_prompt(
                    negative_prompt,
                    negative_prompt_2,
                    self.tokenizer,
                    self.tokenizer_2,
                    self.text_encoder_sess,
                    self.text_encoder_2_sess,
                )

            # Duplicate negative embeds for each generation per prompt
            negative_prompt_embeds = negative_prompt_embeds.repeat(batch_size, 1, 1)
            negative_pooled_prompt_embeds = negative_pooled_prompt_embeds.repeat(
                batch_size, 1
            )

        # Adjust shapes for num_images_per_prompt
        prompt_embeds = prompt_embeds.repeat(1, num_images_per_prompt, 1)
        prompt_embeds = prompt_embeds.view(
            batch_size * num_images_per_prompt, -1, prompt_embeds.shape[-1]
        )
        pooled_prompt_embeds = pooled_prompt_embeds.repeat(1, num_images_per_prompt, 1)
        pooled_prompt_embeds = pooled_prompt_embeds.view(
            batch_size * num_images_per_prompt, -1
        )

        if do_classifier_free_guidance:
            negative_prompt_embeds = negative_prompt_embeds.repeat(
                1, num_images_per_prompt, 1
            )
            negative_prompt_embeds = negative_prompt_embeds.view(
                batch_size * num_images_per_prompt, -1, negative_prompt_embeds.shape[-1]
            )
            negative_pooled_prompt_embeds = negative_pooled_prompt_embeds.repeat(
                1, num_images_per_prompt, 1
            )
            negative_pooled_prompt_embeds = negative_pooled_prompt_embeds.view(
                batch_size * num_images_per_prompt, -1
            )

        # Set dtype and device

        prompt_embeds = prompt_embeds.to(dtype=torch.float16, device=device)
        pooled_prompt_embeds = pooled_prompt_embeds.to(
            dtype=torch.float16, device=device
        )
        if do_classifier_free_guidance:
            negative_prompt_embeds = negative_prompt_embeds.to(
                dtype=torch.float16, device=device
            )
            negative_pooled_prompt_embeds = negative_pooled_prompt_embeds.to(
                dtype=torch.float16, device=device
            )

        # Unscale LoRA layers if necessary
        if isinstance(self, StableDiffusionXLLoraLoaderMixin) and USE_PEFT_BACKEND:
            unscale_lora_layers(self.text_encoder, lora_scale)
            unscale_lora_layers(self.text_encoder_2, lora_scale)

        return (
            prompt_embeds,
            negative_prompt_embeds,
            pooled_prompt_embeds,
            negative_pooled_prompt_embeds,
        )

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.encode_image
    def encode_image(self, image, device, num_images_per_prompt):
        dtype = next(self.image_encoder.parameters()).dtype

        if not isinstance(image, torch.Tensor):
            image = self.feature_extractor(image, return_tensors="pt").pixel_values

        image = image.to(device=device, dtype=dtype)
        image_embeds = self.image_encoder(image).image_embeds
        image_embeds = image_embeds.repeat_interleave(num_images_per_prompt, dim=0)

        uncond_image_embeds = torch.zeros_like(image_embeds)
        return image_embeds, uncond_image_embeds

    def predict_unet(
        self,
        prompt_embeds,
        negative_prompt_embeds,
        pooled_prompt_embeds,
        negative_pooled_prompt_embeds,
        num_inference_steps,
        timesteps,
        num_images_per_prompt,
        height,
        width,
        guidance_scale,
        device,
        generator,
        latents=None,
        eta=0.0,
        cache_interval=3,
        uniform=True,
        center=None,
        pow=None,
        callback=None,
        callback_steps=1,
        **kwargs,
    ):
        device = device or self._execution_device
        timesteps, num_inference_steps = retrieve_timesteps(
            self.scheduler, num_inference_steps, device, timesteps
        )

        # Setup DeepCache interval sequence
        if cache_interval == 1:
            interval_seq = list(range(num_inference_steps))
        else:
            if uniform:
                interval_seq = list(range(0, num_inference_steps, cache_interval))
            else:
                num_slow_step = num_inference_steps // cache_interval
                if num_inference_steps % cache_interval != 0:
                    num_slow_step += 1
                interval_seq, pow = sample_from_quad_center(num_inference_steps, num_slow_step, center=center, pow=pow)
        
        self.enable_deepcache(interval_seq)

        num_channels_latents = self.unet_config["in_channels"]
        latents = self.prepare_latents(
            prompt_embeds.shape[0] * num_images_per_prompt,
            num_channels_latents,
            height,
            width,
            prompt_embeds.dtype,
            device,
            generator,
            latents,
        )

        extra_step_kwargs = self.prepare_extra_step_kwargs(generator, eta)

        add_text_embeds = pooled_prompt_embeds
        text_encoder_projection_dim = self.text_encoder_2_config["projection_dim"]

        add_time_ids = self._get_add_time_ids(
            (height, width),
            (0, 0),
            (height, width),
            dtype=prompt_embeds.dtype,
            text_encoder_projection_dim=text_encoder_projection_dim,
        )

        if self.do_classifier_free_guidance:
            prompt_embeds = torch.cat([negative_prompt_embeds, prompt_embeds], dim=0)
            add_text_embeds = torch.cat(
                [negative_pooled_prompt_embeds, add_text_embeds], dim=0
            )
            add_time_ids = add_time_ids.repeat(2, 1)

        prompt_embeds = prompt_embeds.to(device)
        add_text_embeds = add_text_embeds.to(device)
        add_time_ids = add_time_ids.to(device).repeat(prompt_embeds.shape[0], 1)

        num_warmup_steps = max(
            len(timesteps) - num_inference_steps * self.scheduler.order, 0
        )

        timestep_cond = None
        if self.unet_config.get("time_cond_proj_dim") is not None:
            guidance_scale_tensor = torch.tensor(guidance_scale - 1).repeat(
                prompt_embeds.shape[0]
            )
            timestep_cond = self.get_guidance_scale_embedding(
                guidance_scale_tensor,
                embedding_dim=self.unet_config["time_cond_proj_dim"],
            ).to(device=device, dtype=latents.dtype)

        start_time = time.perf_counter()
        unet_time_device = 0

        with self.progress_bar(total=num_inference_steps) as progress_bar:
            for i, t in enumerate(timesteps):
                latent_model_input = (
                    torch.cat([latents] * 2)
                    if self.do_classifier_free_guidance
                    else latents
                )
                latent_model_input = self.scheduler.scale_model_input(latent_model_input, t)

                added_cond_kwargs = {
                    "text_embeds": add_text_embeds,
                    "time_ids": add_time_ids,
                }

                start_time_device = time.perf_counter()
                noise_pred = self._unet_forward(
                    latent_model_input, t, prompt_embeds, added_cond_kwargs, step_index=i
                )
                end_time_device = time.perf_counter()
                unet_time_device += (end_time_device - start_time_device)
                print(f'UNet (device) time at step {i}: {1000.*(end_time_device - start_time_device):.6f} ms')

                if self.do_classifier_free_guidance:
                    noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
                    noise_pred = noise_pred_uncond + guidance_scale * (
                        noise_pred_text - noise_pred_uncond
                    )

                if self.do_classifier_free_guidance and self.guidance_rescale > 0.0:
                    noise_pred = rescale_noise_cfg(noise_pred, noise_pred_text)

                latents = self.scheduler.step(
                    noise_pred, t, latents, **extra_step_kwargs, return_dict=False
                )[0]

                if i == len(timesteps) - 1 or ((i + 1) > num_warmup_steps and (i + 1) % self.scheduler.order == 0):
                    progress_bar.update()
                    if callback is not None and i % callback_steps == 0:
                        callback(i, t, latents)

        print(f'UNet total time (device) : {1000.* unet_time_device:.6f} ms')
        print(f'UNet total time : {1000.*(time.perf_counter()-start_time):.6f} ms')

        return latents

    def _unet_forward(self, latent_model_input, t, prompt_embeds, added_cond_kwargs, step_index=None):
        is_deepcache = isinstance(self.unet_sess, tuple)
        use_big_model = not is_deepcache or (step_index in self.interval_seq)
        print(f'----is_deepcache: {is_deepcache}, use_big_model: {use_big_model}')
        if is_deepcache:
            #TODO: this time it is with shape (2,6)
            if self.unet_sess2 is None:
                time_ids_input = added_cond_kwargs["time_ids"][:2]
            else:
                time_ids_input = added_cond_kwargs["time_ids"]

            if use_big_model:
                inputname_list = [
                    "sample",
                    "timestep",
                    "encoder_hidden_states",
                    "text_embeds",
                    "time_ids",
                ]
                tensor_input_list = [
                    latent_model_input,
                    torch.Tensor([t]),
                    prompt_embeds,
                    added_cond_kwargs["text_embeds"],
                    time_ids_input,
                ]
            else:
                inputname_list = [
                    "sample",
                    "timestep",
                    "replicate_prv_feature",
                    "text_embeds",
                    "time_ids",
                ]
                tensor_input_list = [
                    latent_model_input,
                    torch.Tensor([t]),
                    self.prv_features,
                    added_cond_kwargs["text_embeds"],
                    time_ids_input,
                ]
        else:
            inputname_list = [
                "sample",
                "timestep",
                "encoder_hidden_states",
                "text_embeds",
                "time_ids",
            ]
            if self.unet_sess2 is None:
                time_ids_input = added_cond_kwargs["time_ids"][:2]
                tensor_input_list = [
                    latent_model_input,
                    torch.Tensor([t]),
                    prompt_embeds,
                    added_cond_kwargs["text_embeds"],
                    time_ids_input,
                ]
            else:
                tensor_input_list = [
                    latent_model_input,
                    torch.Tensor([t]),
                    prompt_embeds,
                    added_cond_kwargs["text_embeds"],
                    added_cond_kwargs["time_ids"],
                ]

        if self.unet_sess2 is None:  # Single device mode
            # Handle both normal session and DeepCache tuple cases
            if isinstance(self.unet_sess, tuple):
                current_sess = self.unet_sess[0] if use_big_model else self.unet_sess[1]
            else:
                current_sess = self.unet_sess

            input_dict = {
                inputname: tensor_input.numpy().astype(
                    current_sess.model_input_shape_dict[inputname][1]
                )
                for inputname, tensor_input in zip(inputname_list, tensor_input_list)
            }
            output = current_sess.run(input_dict)
            o_shape, o_type = current_sess.model_output_shape_dict["out_sample"]
            noise_pred = torch.from_numpy(
                np.frombuffer(output["out_sample"], dtype=o_type).reshape(o_shape)
            )
            
            if is_deepcache:
                if "replicate_prv_feature_RetainedState" not in output:
                    raise ValueError("replicate_prv_feature_RetainedState not in output with deepcache mode, please investigate!! ONNX generation might be wrong")
                p_shape, p_type = current_sess.model_output_shape_dict["replicate_prv_feature_RetainedState"]
                self.prv_features = torch.from_numpy(
                    np.frombuffer(output["replicate_prv_feature_RetainedState"], dtype=p_type).reshape(p_shape)
                )
        else:  # Dual device mode
            # Handle both normal sessions and DeepCache tuple cases
            if isinstance(self.unet_sess, tuple):
                current_sess_pos = self.unet_sess[0] if use_big_model else self.unet_sess[1]
                current_sess_neg = self.unet_sess2[0] if use_big_model else self.unet_sess2[1]
            else:
                current_sess_pos = self.unet_sess
                current_sess_neg = self.unet_sess2

            input_dict = {
                inputname: tensor_input[0:1].numpy().astype(
                    current_sess_pos.model_input_shape_dict[inputname][1]
                )
                if inputname != "timestep"
                else tensor_input.numpy().astype(
                    current_sess_pos.model_input_shape_dict[inputname][1]
                )
                for inputname, tensor_input in zip(inputname_list, tensor_input_list)
            }
            input_dict2 = {
                inputname: tensor_input[1:2].numpy().astype(
                    current_sess_neg.model_input_shape_dict[inputname][1]
                )
                if inputname != "timestep"
                else tensor_input.numpy().astype(
                    current_sess_neg.model_input_shape_dict[inputname][1]
                )
                for inputname, tensor_input in zip(inputname_list, tensor_input_list)
            }

            future_1 = self.executor.submit(current_sess_pos.run, input_dict)
            future_2 = self.executor.submit(current_sess_neg.run, input_dict2)
            result1, result2 = future_1.result(), future_2.result()

            o_shape, o_type = current_sess_pos.model_output_shape_dict["out_sample"]
            noise_pred = torch.from_numpy(
                np.concatenate(
                    (
                        np.frombuffer(result1["out_sample"], dtype=o_type).reshape(o_shape),
                        np.frombuffer(result2["out_sample"], dtype=o_type).reshape(o_shape),
                    ),
                    axis=0,
                )
            )
            
            if is_deepcache and "replicate_prv_feature_RetainedState" in result1:
                p_shape, p_type = current_sess_pos.model_output_shape_dict["replicate_prv_feature_RetainedState"]
                self.prv_features = torch.from_numpy(
                    np.concatenate(
                        (
                            np.frombuffer(result1["replicate_prv_feature_RetainedState"], dtype=p_type).reshape(p_shape),
                            np.frombuffer(result2["replicate_prv_feature_RetainedState"], dtype=p_type).reshape(p_shape),
                        ),
                        axis=0,
                    )
                )

        return noise_pred

    def predict_vae(self, latents, output_type="pil", vae_decoder_sess=None):
        if not output_type == "latent":
            needs_upcasting = (
                torch.float16 == torch.float16 and self.vae_config["force_upcast"]
            )

            input_dict = {
                "latent_sample": latents.numpy() / self.vae_config["scaling_factor"]
            }

            if self.vae_decoder_sess is None:
                raise ValueError("vae_decoder_sess is None")

            o_shape, o_type = self.vae_decoder_sess.model_output_shape_dict["sample"]
            output = self.vae_decoder_sess.run(input_dict)
            image = torch.from_numpy(
                np.frombuffer(output["sample"], dtype=o_type).reshape(o_shape)
            )
            # if needs_upcasting:
            #     self.vae.to(dtype=torch.float16)
        else:
            image = latents

        if not output_type == "latent":
            image = self.image_processor.postprocess(image, output_type=output_type)

        return image

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.prepare_extra_step_kwargs
    def prepare_extra_step_kwargs(self, generator, eta):
        # prepare extra kwargs for the scheduler step, since not all schedulers have the same signature
        # eta (η) is only used with the DDIMScheduler, it will be ignored for other schedulers.
        # eta corresponds to η in DDIM paper: https://arxiv.org/abs/2010.02502
        # and should be between [0, 1]

        accepts_eta = "eta" in set(
            inspect.signature(self.scheduler.step).parameters.keys()
        )
        extra_step_kwargs = {}
        if accepts_eta:
            extra_step_kwargs["eta"] = eta

        # check if the scheduler accepts generator
        accepts_generator = "generator" in set(
            inspect.signature(self.scheduler.step).parameters.keys()
        )
        if accepts_generator:
            extra_step_kwargs["generator"] = generator
        return extra_step_kwargs

    def check_inputs(
        self,
        prompt,
        prompt_2,
        height,
        width,
        callback_steps,
        negative_prompt=None,
        negative_prompt_2=None,
        prompt_embeds=None,
        negative_prompt_embeds=None,
        pooled_prompt_embeds=None,
        negative_pooled_prompt_embeds=None,
        callback_on_step_end_tensor_inputs=None,
    ):
        if height % 8 != 0 or width % 8 != 0:
            raise ValueError(
                f"`height` and `width` have to be divisible by 8 but are {height} and {width}."
            )

        if callback_steps is not None and (
            not isinstance(callback_steps, int) or callback_steps <= 0
        ):
            raise ValueError(
                f"`callback_steps` has to be a positive integer but is {callback_steps} of type"
                f" {type(callback_steps)}."
            )

        if callback_on_step_end_tensor_inputs is not None and not all(
            k in self._callback_tensor_inputs
            for k in callback_on_step_end_tensor_inputs
        ):
            raise ValueError(
                f"`callback_on_step_end_tensor_inputs` has to be in {self._callback_tensor_inputs}, but found {[k for k in callback_on_step_end_tensor_inputs if k not in self._callback_tensor_inputs]}"
            )

        if prompt is not None and prompt_embeds is not None:
            raise ValueError(
                f"Cannot forward both `prompt`: {prompt} and `prompt_embeds`: {prompt_embeds}. Please make sure to"
                " only forward one of the two."
            )
        elif prompt_2 is not None and prompt_embeds is not None:
            raise ValueError(
                f"Cannot forward both `prompt_2`: {prompt_2} and `prompt_embeds`: {prompt_embeds}. Please make sure to"
                " only forward one of the two."
            )
        elif prompt is None and prompt_embeds is None:
            raise ValueError(
                "Provide either `prompt` or `prompt_embeds`. Cannot leave both `prompt` and `prompt_embeds` undefined."
            )
        elif prompt is not None and (
            not isinstance(prompt, str) and not isinstance(prompt, list)
        ):
            raise ValueError(
                f"`prompt` has to be of type `str` or `list` but is {type(prompt)}"
            )
        elif prompt_2 is not None and (
            not isinstance(prompt_2, str) and not isinstance(prompt_2, list)
        ):
            raise ValueError(
                f"`prompt_2` has to be of type `str` or `list` but is {type(prompt_2)}"
            )

        if negative_prompt is not None and negative_prompt_embeds is not None:
            raise ValueError(
                f"Cannot forward both `negative_prompt`: {negative_prompt} and `negative_prompt_embeds`:"
                f" {negative_prompt_embeds}. Please make sure to only forward one of the two."
            )
        elif negative_prompt_2 is not None and negative_prompt_embeds is not None:
            raise ValueError(
                f"Cannot forward both `negative_prompt_2`: {negative_prompt_2} and `negative_prompt_embeds`:"
                f" {negative_prompt_embeds}. Please make sure to only forward one of the two."
            )

        if prompt_embeds is not None and negative_prompt_embeds is not None:
            if prompt_embeds.shape != negative_prompt_embeds.shape:
                raise ValueError(
                    "`prompt_embeds` and `negative_prompt_embeds` must have the same shape when passed directly, but"
                    f" got: `prompt_embeds` {prompt_embeds.shape} != `negative_prompt_embeds`"
                    f" {negative_prompt_embeds.shape}."
                )

        if prompt_embeds is not None and pooled_prompt_embeds is None:
            raise ValueError(
                "If `prompt_embeds` are provided, `pooled_prompt_embeds` also have to be passed. Make sure to generate `pooled_prompt_embeds` from the same text encoder that was used to generate `prompt_embeds`."
            )

        if negative_prompt_embeds is not None and negative_pooled_prompt_embeds is None:
            raise ValueError(
                "If `negative_prompt_embeds` are provided, `negative_pooled_prompt_embeds` also have to be passed. Make sure to generate `negative_pooled_prompt_embeds` from the same text encoder that was used to generate `negative_prompt_embeds`."
            )

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.prepare_latents
    def prepare_latents(
        self,
        batch_size,
        num_channels_latents,
        height,
        width,
        dtype,
        device,
        generator,
        latents=None,
    ):
        shape = (
            batch_size,
            num_channels_latents,
            height // self.vae_scale_factor,
            width // self.vae_scale_factor,
        )
        if isinstance(generator, list) and len(generator) != batch_size:
            raise ValueError(
                f"You have passed a list of generators of length {len(generator)}, but requested an effective batch"
                f" size of {batch_size}. Make sure the batch size matches the length of the generators."
            )

        if latents is None:
            latents = randn_tensor(
                shape, generator=generator, device=device, dtype=dtype
            )
        else:
            latents = latents.to(device)

        # scale the initial noise by the standard deviation required by the scheduler
        latents = latents * self.scheduler.init_noise_sigma
        return latents

    def _get_add_time_ids(
        self,
        original_size,
        crops_coords_top_left,
        target_size,
        dtype,
        text_encoder_projection_dim=None,
    ):
        add_time_ids = list(original_size + crops_coords_top_left + target_size)

        passed_add_embed_dim = (
            self.unet_config["addition_time_embed_dim"] * len(add_time_ids)
            + text_encoder_projection_dim
        )
        expected_add_embed_dim = (
            self.expected_add_embed_dim
        )  # self.unet.add_embedding.linear_1.in_features

        if expected_add_embed_dim != passed_add_embed_dim:
            raise ValueError(
                f"Model expects an added time embedding vector of length {expected_add_embed_dim}, but a vector of {passed_add_embed_dim} was created. The model has an incorrect config. Please check `unet.config.time_embedding_type` and `text_encoder_2.config.projection_dim`."
            )

        add_time_ids = torch.tensor([add_time_ids], dtype=dtype)
        return add_time_ids

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion_upscale.StableDiffusionUpscalePipeline.upcast_vae
    def upcast_vae(self):
        dtype = self.vae.dtype
        self.vae.to(dtype=torch.float32)
        use_torch_2_0_or_xformers = isinstance(
            self.vae.decoder.mid_block.attentions[0].processor,
            (
                AttnProcessor2_0,
                XFormersAttnProcessor,
                LoRAXFormersAttnProcessor,
                LoRAAttnProcessor2_0,
            ),
        )
        # if xformers or torch_2_0 is used attention block does not need
        # to be in float32 which can save lots of memory
        if use_torch_2_0_or_xformers:
            self.vae.post_quant_conv.to(dtype)
            self.vae.decoder.conv_in.to(dtype)
            self.vae.decoder.mid_block.to(dtype)

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.enable_freeu
    def enable_freeu(self, s1: float, s2: float, b1: float, b2: float):
        r"""Enables the FreeU mechanism as in https://arxiv.org/abs/2309.11497.

        The suffixes after the scaling factors represent the stages where they are being applied.

        Please refer to the [official repository](https://github.com/ChenyangSi/FreeU) for combinations of the values
        that are known to work well for different pipelines such as Stable Diffusion v1, v2, and Stable Diffusion XL.

        Args:
            s1 (`float`):
                Scaling factor for stage 1 to attenuate the contributions of the skip features. This is done to
                mitigate "oversmoothing effect" in the enhanced denoising process.
            s2 (`float`):
                Scaling factor for stage 2 to attenuate the contributions of the skip features. This is done to
                mitigate "oversmoothing effect" in the enhanced denoising process.
            b1 (`float`): Scaling factor for stage 1 to amplify the contributions of backbone features.
            b2 (`float`): Scaling factor for stage 2 to amplify the contributions of backbone features.
        """
        if not hasattr(self, "unet"):
            raise ValueError("The pipeline must have `unet` for using FreeU.")
        self.unet.enable_freeu(s1=s1, s2=s2, b1=b1, b2=b2)

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.disable_freeu
    def disable_freeu(self):
        """Disables the FreeU mechanism if enabled."""
        self.unet.disable_freeu()

    # Copied from diffusers.pipelines.latent_consistency_models.pipeline_latent_consistency_text2img.LatentConsistencyModelPipeline.get_guidance_scale_embedding
    def get_guidance_scale_embedding(self, w, embedding_dim=512, dtype=torch.float32):
        """
        See https://github.com/google-research/vdm/blob/dc27b98a554f65cdc654b800da5aa1846545d41b/model_vdm.py#L298

        Args:
            timesteps (`torch.Tensor`):
                generate embedding vectors at these timesteps
            embedding_dim (`int`, *optional*, defaults to 512):
                dimension of the embeddings to generate
            dtype:
                data type of the generated embeddings

        Returns:
            `torch.FloatTensor`: Embedding vectors with shape `(len(timesteps), embedding_dim)`
        """
        assert len(w.shape) == 1
        w = w * 1000.0

        half_dim = embedding_dim // 2
        emb = torch.log(torch.tensor(10000.0)) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, dtype=dtype) * -emb)
        emb = w.to(dtype)[:, None] * emb[None, :]
        emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1)
        if embedding_dim % 2 == 1:  # zero pad
            emb = torch.nn.functional.pad(emb, (0, 1))
        assert emb.shape == (w.shape[0], embedding_dim)
        return emb

    @torch.no_grad()
    # @replace_example_docstring(EXAMPLE_DOC_STRING)
    def __call__(
        self,
        prompt: Union[str, List[str]] = None,
        prompt_2: Optional[Union[str, List[str]]] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        num_inference_steps: int = 50,
        timesteps: List[int] = None,
        denoising_end: Optional[float] = None,
        guidance_scale: float = 5.0,
        negative_prompt: Optional[Union[str, List[str]]] = None,
        negative_prompt_2: Optional[Union[str, List[str]]] = None,
        num_images_per_prompt: Optional[int] = 1,
        eta: float = 0.0,
        generator: Optional[Union[torch.Generator, List[torch.Generator]]] = None,
        latents: Optional[torch.FloatTensor] = None,
        prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_prompt_embeds: Optional[torch.FloatTensor] = None,
        pooled_prompt_embeds: Optional[torch.FloatTensor] = None,
        negative_pooled_prompt_embeds: Optional[torch.FloatTensor] = None,
        ip_adapter_image: Optional[PipelineImageInput] = None,
        output_type: Optional[str] = "pil",
        return_dict: bool = True,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        guidance_rescale: float = 0.0,
        original_size: Optional[Tuple[int, int]] = None,
        crops_coords_top_left: Tuple[int, int] = (0, 0),
        target_size: Optional[Tuple[int, int]] = None,
        negative_original_size: Optional[Tuple[int, int]] = None,
        negative_crops_coords_top_left: Tuple[int, int] = (0, 0),
        negative_target_size: Optional[Tuple[int, int]] = None,
        clip_skip: Optional[int] = None,
        callback_on_step_end: Optional[Callable[[int, int, Dict], None]] = None,
        callback_on_step_end_tensor_inputs: List[str] = ["latents"],
        **kwargs,
    ):
        # 0. Default height and width to unet
        height = height or self.default_sample_size * self.vae_scale_factor
        width = width or self.default_sample_size * self.vae_scale_factor

        # 1. Check inputs
        self.check_inputs(
            prompt,
            height,
            width,
            callback_steps,
            negative_prompt,
            prompt_embeds,
            negative_prompt_embeds,
        )

        # 2. Define call parameters
        if prompt is not None and isinstance(prompt, str):
            batch_size = 1
        elif prompt is not None and isinstance(prompt, list):
            batch_size = len(prompt)
        else:
            batch_size = prompt_embeds.shape[0]

        device = self._execution_device

        # 3. Encode input prompt
        (
            prompt_embeds,
            negative_prompt_embeds,
            pooled_prompt_embeds,
            negative_pooled_prompt_embeds,
        ) = self.encode_prompt(
            prompt,
            device,
            num_images_per_prompt,
            do_classifier_free_guidance=guidance_scale > 1.0,
            negative_prompt=negative_prompt,
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_prompt_embeds,
            pooled_prompt_embeds=pooled_prompt_embeds,
            negative_pooled_prompt_embeds=negative_pooled_prompt_embeds,
        )

        # 4. Prepare timesteps
        self.scheduler.set_timesteps(num_inference_steps, device=device)
        timesteps = self.scheduler.timesteps
        print(device, timesteps)

        # # 5. Prepare latent variables
        # num_channels_latents = self.unet_config.in_channels
        # latents = self.prepare_latents(
        #     batch_size * num_images_per_prompt,
        #     num_channels_latents,
        #     height,
        #     width,
        #     prompt_embeds.dtype,
        #     device,
        #     generator,
        #     latents,
        # )

        # 6. Run UNet
        latents = self.predict_unet(
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_prompt_embeds,
            pooled_prompt_embeds=pooled_prompt_embeds,
            negative_pooled_prompt_embeds=negative_pooled_prompt_embeds,
            num_inference_steps=num_inference_steps,
            timesteps=timesteps,
            num_images_per_prompt=num_images_per_prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            device=device,
            generator=generator,
            latents=latents,
            eta=eta,
            original_size=original_size,
            crops_coords_top_left=crops_coords_top_left,
            target_size=target_size,
            guidance_rescale=guidance_rescale,
            cross_attention_kwargs=cross_attention_kwargs,
        )
        #TODO: add cache_interval=3, (add deepcache params)
        # uniform=True,
        # center=None,
        # pow=None,

        # 7. Run VAE
        images = self.predict_vae(latents, output_type=output_type)

        # 8. Postprocess
        if self.watermark is not None:
            images = self.watermark.apply_watermark(images)

        if not return_dict:
            return (images,)

        return StableDiffusionXLPipelineOutput(images=images)
