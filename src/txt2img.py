from helpers.model_loader import ModelLoader
from helpers.storage_helper import StorageHelper


class Txt2Img():

    @staticmethod
    def create_with_model(number_of_images: int, model_id: str, cuda_id: int) -> None:
        model = ModelLoader.get_txt2img_model(model_id, cuda_id)
        for word in StorageHelper.words:
            for i in range(number_of_images):
                image = model.generate_image([word])[0]
                StorageHelper.save_image(image, f'{word}_{i}')
