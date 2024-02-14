import torch
from diffusers.pipelines.auto_pipeline import AutoPipelineForText2Image
from PIL.Image import Image

from resources.txt2img_models.txt2img_model import Txt2ImgModel


class SDXLTurbo(Txt2ImgModel):

    def __init__(self, cuda_id: int) -> None:
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path='stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16').to(cuda_id)

    def generate_image(self, prompt: list[str]) -> list[Image]:
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=0, num_inference_steps=3).images
