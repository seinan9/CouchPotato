import torch
from diffusers import AutoPipelineForText2Image

class ImageGenerator:

    def __init__(self, model_id: str = "stabilityai/sdxl-turbo"):
        self.__pipeline = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16").to("cuda:1")
    
    def generate_images(self, prompt: list[str], num_inference_steps: int = 4):
        with torch.no_grad():
            return self.__pipeline(prompt=prompt, guidance_scale=0.0, num_inference_steps=num_inference_steps).images

if __name__ == "__main__":
    model_id = "stabilityai/sdxl-turbo"
    ig = ImageGenerator()
    prompt = ["A cat playing with a red ball, black fur, cute, adorable, Pixar, Disney."]
    images = ig.generate_images(prompt)
    images[0].save("ig-output.png")
