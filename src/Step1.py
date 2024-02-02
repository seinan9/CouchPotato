from Loader import Loader
from StorageHelper import StorageHelper
from image_generators.ImageGenerator import ImageGenerator


class Step1():

    def __init__(self, params):
        self.compound = params["0"]["compound"]
        self.constituents = params["0"]["constituents"]

        self.output_dir = params["1"]["output_dir"]
        self.n_images = params["1"]["n_images"]
        self.image_generator_id = params["1"]["image_generator_id"]
        self.image_generator_params = params["1"]["image_generator_params"]

    def generate_simple_dataset(self):
        image_generator = Loader.get_image_generator(self.image_generator_id)
        for word in [self.compound] + self.constituents:
            for n in range(self.n_images):
                image = image_generator.generate_image([f'{word}'])
                StorageHelper.save_image(f'{self.output_dir}/{word}_{n}.png')
