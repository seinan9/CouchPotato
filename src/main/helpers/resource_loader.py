import importlib

from resources.img2vec_models.img2vec_model import Img2VecModel
from resources.txt2img_models.txt2img_model import Txt2ImgModel
from resources.ved2dist_measures.vec2dist_measure import Vec2DistMeasure
from resources.txt2vec_models.txt2vec_model import Txt2VecModel


class ResourceLoader():

    @staticmethod
    def get_txt2img_model(model_id: str, cuda_id: int) -> Txt2ImgModel:
        module = importlib.import_module(
            f'resources.txt2img_models.{model_id.lower()}')
        return getattr(module, model_id)(cuda_id)

    @staticmethod
    def get_img2vec_model(model_id: str, cuda_id) -> Img2VecModel:
        module = importlib.import_module(
            f'resources.img2vec_models.{model_id.lower()}')
        return getattr(module, model_id)(cuda_id)

    @staticmethod
    def get_vec2dist_measure(measure_id: str) -> Vec2DistMeasure:
        module = importlib.import_module(
            f'resources.ved2dist_measures.{measure_id.lower()}')
        return getattr(module, measure_id)()

    @staticmethod
    def get_txt2vec_model(model_id: str) -> Txt2VecModel:
        module = importlib.import_module(
            f'resources.txt2vec_models.{model_id.lower()}')
        return getattr(module, model_id)()
