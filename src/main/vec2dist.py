import torch

from helpers.resource_loader import ResourceLoader
from helpers.storage_helper import StorageHelper


class Vec2Dist():

    @staticmethod
    def aggregate_with_mean(measure_id: str) -> None:
        measure = ResourceLoader.get_vec2dist_measure(measure_id)
        vectors = StorageHelper.load_all_vectors()
        mean_vectors = {f'{word}': torch.mean(
            vectors[word], dim=0) for word in StorageHelper.words}
        distances = {f'{constituent}': measure.calculate(
            mean_vectors[StorageHelper.words[0]], mean_vectors[constituent]) for constituent in StorageHelper.words[1:]}
        StorageHelper.save_distances(distances, 'mean')
