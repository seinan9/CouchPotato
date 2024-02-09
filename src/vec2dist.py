import torch

from helpers.storage_helper import StorageHelper


class Vec2Dist():

    @staticmethod
    def do(params):
        compound = params[0]
        constituents = params[1]
        file_names_separated = {f'{word}': []
                                for word in [compound] + constituents}

        file_names = StorageHelper.list_files('vectors')
        for file_name in file_names:
            for word in file_names_separated.keys():
                if word in file_name:
                    file_names_separated[word].append(file_name)
                    break

        vectors = {f'{word}': torch.stack([StorageHelper.load_vec(
            file_name) for file_name in file_names_separated[word]]) for word in [compound] + constituents}

        results = Vec2Dist.aggregate_mean(compound, constituents, vectors)
        print(results)

    @staticmethod
    def aggregate_mean(compound, constituents, vectors):
        mean_vectors = {f'{word}': torch.mean(vectors[word], dim=0) for word in [
            compound] + constituents}

        return {f'{constituent}': Vec2Dist.cos(
            mean_vectors[compound], mean_vectors[constituent]) for constituent in constituents}

    @staticmethod
    def cos(vec_0, vec_1):
        return torch.cosine_similarity(vec_0, vec_1, dim=0).numpy().tolist()
