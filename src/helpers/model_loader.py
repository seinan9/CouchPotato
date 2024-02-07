import importlib

from models.word2img_model import Word2ImgModel
from models.img2vec_model import Img2VecModel


class ModelLoader():

    @staticmethod
    def get_word2img_model(word2img_model_id: str) -> Word2ImgModel:
        module = importlib.import_module(f'models.{word2img_model_id.lower()}')
        return getattr(module, word2img_model_id)()

    @staticmethod
    def get_img2vec_model(img2vec_model_id: str) -> Img2VecModel:
        module = importlib.import_module(
            f'embedding_generators.{img2vec_model_id.lower()}')
        return getattr(module, img2vec_model_id)()

    # @staticmethod
    # def get_distance_generator(id: str) -> DistanceGenerator:
    #     module = importlib.import_module(f'distance_generators.{id}')
    #     distance_generator = getattr(module, id)()
    #     return distance_generator
