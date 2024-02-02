from diffusers import AutoPipelineForText2Image
import torch

from image_generators.ImageGenerator import ImageGenerator


class SDXLTurbo(ImageGenerator):

    # Model parameters
    model_id = "stabilityai/sdxl-turbo"
    torch_dtype = torch.float16
    variant = "fp16"
    cuda_id = 0

    # Inference parameters
    num_inference_steps = 3
    guidance_scale = 0

    def __init__(self):
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(
            pretrained_model_or_path=self.model_id, torch_dtype=self.torch_dtype, variant=self.variant).to(f"cuda:{self.cuda_id}")

    def generate_image(self, prompt: list[str]):
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=self.guidance_scale, num_inference_steps=self.num_inference_steps).images
