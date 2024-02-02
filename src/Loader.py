import importlib
from image_generators.ImageGenerator import ImageGenerator
from embedding_generators.EmbeddingGenerator import EmbeddingGenerator

class Loader():

    @staticmethod
    def get_image_generator(id) -> ImageGenerator:
        module = importlib.import_module(f'image_generators.{id}')
        image_generator = getattr(module, id)()
        return image_generator

    @staticmethod
    def get_embedding_generator(id) -> EmbeddingGenerator:
        module = importlib.import_module(f'embedding_generators.{id}')
        embedding_generator = getattr(module, id)
        return embedding_generator
