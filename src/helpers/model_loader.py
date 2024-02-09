import importlib

from models.img2vec_model import Img2VecModel
from models.txt2img_model import Txt2ImgModel


class ModelLoader():

    @staticmethod
    def get_txt2img_model(model_id: str, cuda_id: int) -> Txt2ImgModel:
        module = importlib.import_module(f'models.{model_id.lower()}')
        return getattr(module, model_id)(cuda_id)

    @staticmethod
    def get_img2vec_model(model_id: str, cuda_id) -> Img2VecModel:
        module = importlib.import_module(
            f'models.{model_id.lower()}')
        return getattr(module, model_id)(cuda_id)
