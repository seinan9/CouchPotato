import importlib
from image_generators.ImageGenerator import ImageGenerator
from embedding_generators.EmbeddingGenerator import EmbeddingGenerator
from distance_generators.DistanceGenerator import DistanceGenerator


class Loader():

    @staticmethod
    def get_image_generator(id: str) -> ImageGenerator:
        module = importlib.import_module(f'image_generators.{id}')
        image_generator = getattr(module, id)()
        return image_generator

    @staticmethod
    def get_embedding_generator(id: str) -> EmbeddingGenerator:
        module = importlib.import_module(f'embedding_generators.{id}')
        embedding_generator = getattr(module, id)()
        return embedding_generator

    @staticmethod
    def get_distance_generator(id: str) -> DistanceGenerator:
        module = importlib.import_module(f'distance_generators.{id}')
        distance_generator = getattr(module, id)()
        return distance_generator
