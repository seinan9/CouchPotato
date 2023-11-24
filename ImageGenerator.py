from diffusers import StableDiffusionPipeline

class ImageGenerator:

    __pipeline = None
    __images = None

    def __init__(self, directory):
        self.__pipeline = StableDiffusionPipeline.from_pretrained(directory)
    
    def generate_images(self, prompt, num_inference_steps):
        self.__images = self.__pipeline(prompt=prompt, num_inference_steps=num_inference_steps).images

    def show_image(self, index):
        self.__images[index].show()

    def save_image(self, index, file_name):
        self.__images[index].save(f"{file_name}.png")

    def save_all_images(self, directory):
        for i in range(len(self.__images)):
            self.__images[i].save(f"{directory}/{i}.png")
        
if __name__ == "__main__":
    ig = ImageGenerator("./data/models")
    prompt = ["a photo of an astronaut riding a horse"]
    ig.generate_images(prompt, 2)
    ig.save_all_images("./data/output")