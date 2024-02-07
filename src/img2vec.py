from helpers.model_loader import ModelLoader
from helpers.storage_helper import StorageHelper


class Img2Vec():

    # TODO: implement fully
    @staticmethod
    def generate_embeddings(img2vec_model_id, img2vec_model_params):
        img2vec_model = ModelLoader.get_img2vec_model(img2vec_model_id)
        file_names = StorageHelper.list_images()
        for file_name in file_names:
            img = StorageHelper.load_image(file_name)
            vec = img2vec_model.generate_embedding(img)
            StorageHelper.save_vec(vec, file_name.split('.')[0])
