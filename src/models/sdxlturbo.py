from diffusers import AutoPipelineForText2Image
import torch

from models.txt2img_model import Txt2ImgModel


# TODO: add cuda_id argument
class SDXLTurbo(Txt2ImgModel):

    # Inference parameters
    num_inference_steps = 3
    guidance_scale = 0

    def __init__(self) -> None:
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path='stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16').to(f'cuda:{0}')

    def generate_image(self, prompt: list[str]) -> list:
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=0, num_inference_steps=3).images
