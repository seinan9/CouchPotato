import torch

from helpers.storage_helper import StorageHelper

class Vec2Vec():
    
    @staticmethod
    def concat() -> None:
        StorageHelper.set_approach('visual')
        image_vectors = StorageHelper.load_all_vectors()
        image_vectors_mean = {f'{word}': torch.mean(image_vectors[word], dim=0) for word in StorageHelper.words}

        StorageHelper.set_approach('textual')
        text_vectors = StorageHelper.load_all_vectors()

        StorageHelper.set_approach('combined')
        for word in StorageHelper.words:
            vector = torch.concat([image_vectors_mean[word], text_vectors[word].squeeze(0)], 0)
            StorageHelper.save_vector(vector, f'{word}_0')
