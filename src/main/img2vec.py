from helpers.resource_loader import ResourceLoader
from helpers.storage_helper import StorageHelper


class Img2Vec():

    @staticmethod
    def create_with_model(model_id: str, cuda_id: int) -> None:
        model = ResourceLoader.get_img2vec_model(model_id, cuda_id)
        file_names = StorageHelper.list_output_files('images')
        for file_name in file_names:
            image = StorageHelper.load_image(file_name)
            vector = model.create_vector(image)
            StorageHelper.save_vector(vector, file_name)
