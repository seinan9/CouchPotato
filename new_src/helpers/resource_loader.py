import importlib

from helpers.utils import Utils
from resources.text_to_image_models.text_to_image_model import TextToImageModel
from resources.image_to_vector_models.image_to_vector_model import ImageToVectorModel

class ResourceLoader():

    @staticmethod
    def load_text_to_image_model(model_id: str, cuda_id: int) -> TextToImageModel:
        module_name = Utils.convert_to_module_name(model_id)
        module = importlib.import_module(
            f'resources.text_to_image_models.{module_name}')
        return getattr(module, model_id)(cuda_id)

    @staticmethod
    def load_image_to_vector_model(model_id: str, cuda_id: int) -> ImageToVectorModel:
        module_name = Utils.convert_to_module_name(model_id)
        module = importlib.import_module(
            f'resources.image_to_vector_models.{module_name}')
        return getattr(module, model_id)(cuda_id)
