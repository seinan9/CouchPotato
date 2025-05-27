from abc import ABC, abstractmethod
from pathlib import Path

import diffusers
import torch
from couch_potato.core.node import Node
from couch_potato.task.utils import load_sentences, load_targets, save_image
from diffusers import PixArtSigmaPipeline, StableDiffusionXLPipeline, Transformer2DModel
from PIL.Image import Image
from tqdm import tqdm


class ImageGenerator(Node):

    PARAMETERS = {
        "output_dir": str,
        "targets": dict | str,
        "prompts_dir": str,
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
        prompts_dir: str,
        seed: int,
        cuda_id: int,
        num_images: int,
        model_name: str,
        steps: int,
        cfg: float,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.prompts_dir = None if prompts_dir in ("", "empty", None) else prompts_dir
        self.seed = seed
        self.num_images = num_images
        self.steps = steps
        self.cfg = cfg
        self.model: TextToImageModel = create_model(model_name, cuda_id)

    def run(self) -> None:
        for compound, constituents in tqdm(
            self.targets.items(), desc="Generating images for targets"
        ):
            compound_output_dir = self.output_dir / compound
            compound_output_dir.mkdir(parents=True)

            for word in [compound] + constituents:
                if self.prompts_dir:
                    file_name = (
                        f"{constituents[0]}_{constituents[1]}"
                        if word == compound
                        else word
                    )
                    prompt_path = self.prompts_dir / file_name
                    prompts = load_sentences(prompt_path)
                    used_prompts = prompts[: self.num_images]
                else:
                    used_prompts = [word] * self.num_images

                for i, prompt in enumerate(used_prompts):
                    image = self.model.generate_image(
                        seed=self.seed + i,
                        prompt=prompt,
                        steps=self.steps,
                        cfg=self.cfg,
                    )
                    out_path = compound_output_dir / f"{word}_{i+1}.png"
                    save_image(image, out_path)


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
