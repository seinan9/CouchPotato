import sys
import torch

from abc import ABC
from abc import abstractmethod
from diffusers.pipelines.auto_pipeline import AutoPipelineForText2Image
import diffusers
from PIL.Image import Image

from core.node import Node
from core.utils import create_dir, join_paths
from task.utils import load_targets, save_image


class SimpleImageGenerator(Node):

    PARAMETERS = {
        'output_dir': str,
        'targets': dict,
        'seed': int,
        'cuda_id': int,
        'num_images': int,
        'model_id': str,
        'steps': int,
        'cfg': float
    }

    def __init__(self, output_dir: str, targets: dict | str, seed: int, cuda_id: int, num_images: int, model_id: str, steps: int, cfg: float) -> None:
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else load_targets(targets)
        self.seed = seed
        self.num_images = num_images
        self.steps = steps
        self.cfg = cfg
        self.model: TextToImageModel = globals()[model_id](cuda_id)

    def run(self) -> None:
        progress = 0
        num_targets = len(self.targets)
        for compound, constituents in self.targets.items():
            progress += 1
            sys.stdout.write(
                f'Processing target {progress} out of {num_targets}\r')
            sys.stdout.flush()

            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)

            for target in [compound] + constituents:
                for i in range(1, self.num_images + 1):
                    image = self.model.generate_image(
                        seed=self.seed + i,
                        prompt=target,
                        steps=self.steps,
                        cfg=self.cfg)
                    image_output_path = join_paths(
                        compound_output_dir, f'{target}_{i}.png')
                    save_image(image, image_output_path)


class TextToImageModel(ABC):

    @abstractmethod
    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        pass


class SdxlTurbo(TextToImageModel):

    def __init__(self, cuda_id: str) -> None:
        diffusers.utils.logging.disable_progress_bar()

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path='stabilityai/sdxl-turbo',
            torch_dtype=torch.float16,
            variant='fp16'
        )
        self.pipe.to(cuda_id)
        self.pipe.set_progress_bar_config(disable=True)

    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        generator = torch.manual_seed(seed)
        with torch.no_grad():
            return self.pipe(
                prompt=prompt,
                num_inference_steps=steps,
                classifier_guidance=cfg,
                generator=generator
            ).images[0]
