from main.visual.ImageGenerator import ImageGenerator

from diffusers import AutoPipelineForText2Image
import torch


class SDXLTurbo():

    # Model parameters
    model_id = "stabilityai/sdxl-turbo"
    torch_dtype = torch.float16
    variant = "fp16"
    cuda_id = 0

    # Inference parameters
    num_inference_steps = 4
    guidance_scale = 0.0

    def __init__(self):
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(
            model_id=self.model_id, torch_dtype=self.torch_dtype, variant=self.variant).to(f"cuda:{self.cuda_id}")

    def generate_image(self, prompt: list[str]):
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=self.guidance_scale, num_inference_steps=self.num_inference_steps).images


if __name__ == "__main__":
    prompt = [
        "A cat playing with a red ball, black fur, cute, adorable, Pixar, Disney"]
    image_generator = SDXLTurbo()
    image_generator.generate_image(prompt)[0].save("cat.png")
