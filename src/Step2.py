from Loader import Loader
from StorageHelper import StorageHelper
from embedding_generators.EmbeddingGenerator import EmbeddingGenerator


class Step2():

    def __init__(self, params):
        self.compound = params["0"]["compound"]
        self.constituents = params["0"]["constituents"]

        self.input_dir = params["2"]["input_dir"]
        self.output_dir = params["2"]["output_dir"]
        self.embedding_generator_id = params["2"]["embedding_generator_id"]
        self.embedding_generator_params = params["2"]["embedding_generator_params"]

    def generate_embeddings(self):
        embedding_generator = Loader.get_embedding_generator(
            self.embedding_generator_id)

        image_generator = Loader.get_image_generator(self.image_generator_id)
        for word in [self.compound] + self.constituents:
            for n in range(self.n_images):
                image = image_generator.generate_image([f'{word}'])
                StorageHelper.save_image(f'{self.output_dir}/{word}_{n}.png')
