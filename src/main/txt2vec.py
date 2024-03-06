from helpers.resource_loader import ResourceLoader
from helpers.storage_helper import StorageHelper


class Txt2Vec():

    @staticmethod
    def create_with_model(model_id: str) -> None:
        model = ResourceLoader.get_txt2vec_model(model_id)
        for word in StorageHelper.words:
            vector = model.create_vector(word)
            StorageHelper.save_vector(vector, f'{word}_0')
