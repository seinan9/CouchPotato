import importlib

from models.txt2img_model import Txt2ImgModel
from models.img2vec_model import Img2VecModel


class ModelLoader():

    @staticmethod
    def get_txt2img_model(txt2img_model_id: str) -> Txt2ImgModel:
        module = importlib.import_module(f'models.{txt2img_model_id.lower()}')
        return getattr(module, txt2img_model_id)()

    @staticmethod
    def get_img2vec_model(img2vec_model_id: str) -> Img2VecModel:
        module = importlib.import_module(
            f'models.{img2vec_model_id.lower()}')
        return getattr(module, img2vec_model_id)()

    # @staticmethod
    # def get_distance_generator(id: str) -> DistanceGenerator:
    #     module = importlib.import_module(f'distance_generators.{id}')
    #     distance_generator = getattr(module, id)()
    #     return distance_generator
