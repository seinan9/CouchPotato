from diffusers import StableDiffusionPipeline

class ImageGenerator:

    def __init__(self, model_id_or_directory: str):
        self.__pipeline = StableDiffusionPipeline.from_pretrained(model_id_or_directory)
    
    def generate_images(self, prompt: list[str], num_inference_steps: int = 50):
        return self.__pipeline(prompt=prompt, num_inference_steps=num_inference_steps).images

if __name__ == "__main__":
    ig = ImageGenerator("./data/models")
    prompt = ["a photo of an astronaut riding a horse"]
    images = ig.generate_images(prompt)
    images[0].show()