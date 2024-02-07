from helpers.model_loader import ModelLoader
from helpers.storage_helper import StorageHelper


# TODO: add model_params
class Word2Img():

    @staticmethod
    def generate_simple_dataset(compound, constituents, num_images, model_id, model_params):
        word2img_model = ModelLoader.get_word2img_model(model_id)
        for word in [compound] + constituents:
            for i in range(num_images):
                image = word2img_model.generate_image([f'{word}'])[0]
                StorageHelper.save_image(image, f'{word}_{i}')
