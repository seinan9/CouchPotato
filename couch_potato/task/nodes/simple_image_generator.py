import logging
from abc import ABC, abstractmethod

import diffusers
import torch
from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import load_targets, save_image
from diffusers import PixArtSigmaPipeline, StableDiffusionXLPipeline, Transformer2DModel
from PIL.Image import Image


class SimpleImageGenerator(Node):

    PARAMETERS = {
        "output_dir": str,
        "targets": dict,
        "seed": int,
        "cuda_id": int,
        "num_images": int,
        "model_name": str,
        "steps": int,
        "cfg": float,
    }

    def __init__(
        self,
        output_dir: str,
        targets: dict | str,
        seed: int,
        cuda_id: int,
        num_images: int,
        model_name: str,
        steps: int,
        cfg: float,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.seed = seed
        self.num_images = num_images
        self.steps = steps
        self.cfg = cfg
        self.model: TextToImageModel = create_model(model_name, cuda_id)

    def run(self) -> None:
        progress = 0
        num_targets = len(self.targets)
        for compound, constituents in self.targets.items():
            progress += 1
            self.logger.progress(f"Processing target {progress} out of {num_targets}")
            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)

            for target in [compound] + constituents:
                for i in range(1, self.num_images + 1):
                    image = self.model.generate_image(
                        seed=self.seed + i,
                        prompt=target,
                        steps=self.steps,
                        cfg=self.cfg,
                    )
                    image_output_path = join_paths(
                        compound_output_dir, f"{target}_{i}.png"
                    )
                    save_image(image, image_output_path)


class TextToImageModel(ABC):

    @abstractmethod
    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        pass


class StableDiffusionXL(TextToImageModel):

    def __init__(self, pretrained_model_name_or_path: str, cuda_id: str) -> None:
        diffusers.utils.logging.disable_progress_bar()

        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            pretrained_model_name_or_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        self.pipe.to(f"cuda:{cuda_id}")
        self.pipe.set_progress_bar_config(disable=True)

    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        generator = torch.manual_seed(seed)
        with torch.no_grad():
            return self.pipe(
                prompt=prompt,
                num_inference_steps=steps,
                classifier_guidance=cfg,
                generator=generator,
                width=1024,
                height=1024,
            ).images[0]


class PixArtSigma(TextToImageModel):

    def __init__(self, cuda_id: str) -> None:
        transformer = Transformer2DModel.from_pretrained(
            pretrained_model_name_or_path="PixArt-alpha/PixArt-Sigma-XL-2-1024-MS",
            subfolder="transformer",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )

        self.pipe = PixArtSigmaPipeline.from_pretrained(
            pretrained_model_name_or_path="PixArt-alpha/pixart_sigma_sdxlvae_T5_diffusers",
            transformer=transformer,
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        self.pipe.to(f"cuda:{cuda_id}")
        self.pipe.set_progress_bar_config(disable=True)

    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        generator = torch.manual_seed(seed)
        with torch.no_grad():
            return self.pipe(
                prompt=prompt,
                num_inference_steps=steps,
                classifier_guidance=cfg,
                generator=generator,
                width=1024,
                height=1024,
            ).images[0]


def create_model(model_name: str, cuda_id: str) -> TextToImageModel:
    if model_name == "sdxl-base":
        return StableDiffusionXL("stabilityai/stable-diffusion-xl-base-1.0", cuda_id)
    elif model_name == "sdxl-juggernaut":
        return StableDiffusionXL("RunDiffusion/Juggernaut-X-v10", cuda_id)
    elif model_name == "pixart-sigma":
        return PixArtSigma(cuda_id)
    else:
        raise ValueError(f"Unknown model name: {model_name}")
