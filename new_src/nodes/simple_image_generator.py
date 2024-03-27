import torch

from abc import ABC
from abc import abstractmethod
from diffusers.pipelines.auto_pipeline import AutoPipelineForText2Image
from PIL.Image import Image

from node import Node
from helpers.storage_helper import StorageHelper


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
            targets, dict) else StorageHelper.load_targets(targets)
        self.seed = seed
        self.num_images = num_images
        self.steps = steps
        self.cfg = cfg
        self.model: TextToImageModel = globals()[model_id](cuda_id)

    def run(self) -> None:
        for compound in self.targets.keys():
            StorageHelper.create_dir(f'{self.output_dir}/{compound}')
            for target in [compound] + self.targets[compound]:
                for i in range(self.num_images):
                    image = self.model.generate_image(
                        seed=self.seed + i,
                        prompt=target,
                        steps=self.steps,
                        cfg=self.cfg)
                    StorageHelper.save_image(
                        image, f'{self.output_dir}/{compound}/{target}_{i}.png')


class TextToImageModel(ABC):

    @abstractmethod
    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        pass


class SdxlTurbo(TextToImageModel):

    def __init__(self, cuda_id: str) -> None:

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path='stabilityai/sdxl-turbo',
            torch_dtype=torch.float16,
            variant='fp16'
        )
        self.pipe.to(cuda_id)

    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        generator = torch.manual_seed(seed)
        with torch.no_grad():
            return self.pipe(
                prompt=prompt,
                num_inference_steps=steps,
                classifier_guidance=cfg,
                generator=generator
            ).images[0]
