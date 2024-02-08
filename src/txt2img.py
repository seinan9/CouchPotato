from helpers.model_loader import ModelLoader
from helpers.storage_helper import StorageHelper


# TODO: add model_params
class Txt2Img():

    @staticmethod
    def generate_simple_dataset(compound, constituents, num_images, txt2img_model_id, txt2img_model_params):
        txt2img_model = ModelLoader.get_txt2img_model(txt2img_model_id)
        for word in [compound] + constituents:
            for i in range(num_images):
                image = txt2img_model.generate_image([f'{word}'])[0]
                StorageHelper.save_image(image, f'{word}_{i}')
