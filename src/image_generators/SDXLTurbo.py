from diffusers import AutoPipelineForText2Image
import torch

from image_generators.ImageGenerator import ImageGenerator


class SDXLTurbo(ImageGenerator):

    # Inference parameters
    num_inference_steps = 3
    guidance_scale = 0

    def __init__(self, cuda_id: int) -> None:
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path='stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16').to(f'cuda:{cuda_id}')

    def generate_image(self, prompt: list[str]) -> list:
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=0, num_inference_steps=3).images
