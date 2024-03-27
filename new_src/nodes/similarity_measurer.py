import os
import torch

from node import Node
from helpers.storage_helper import StorageHelper

class SimilarityMeasurer(Node):

    PARAMETERS = {
        'input_dir': str,
        'output_dir': str,
        'measure': str,
        'dim': int
    }

    def __init__(self, input_dir: str, output_dir: str, targets: dict | str, measure: str, dim: int):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else StorageHelper.load_targets(targets)
        self.measure = getattr(self, measure)
        self.dim = dim


    # TODO: use list_files and regex instead of assuming target_0.pt
    def run(self):
        for compound, constituents in self.targets.items():
            compound_input_dir = os.path.join(self.input_dir, compound)
            compound_input_file = os.path.join(compound_input_dir, f'{compound}
            _0.pt')
            compound_vector = StorageHelper.load_vector(compound_input_file)

            similarities = {}
            for constituent in constituents:
                constituent_input_file = os.path.join(compound_input_dir, f'
                {constituent}_0.pt')
                constituent_vector = StorageHelper.load_vector(constituent_input_file)
                similarities[constituent] = self.measure(compound_vector, constituent_vector)

            compound_output_dir = os.path.join(self.output_dir, compound)
            compound_output_file = os.path.join(compound_output_dir, 'similarities.tsv')

            # TODO: implement function to store results in csv or tsv
            StorageHelper.save_similarities(data, compound_output_file)

    def cosine(self, vector0: torch.Tensor, vector1: torch.Tensor, dim: int) -> float:
        return torch.cosine_similarity(vector0, vector1, dim).item()