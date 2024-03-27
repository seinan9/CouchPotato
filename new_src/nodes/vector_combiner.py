import os
import re
import torch

from node import Node
from helpers.storage_helper import StorageHelper


class VectorCombiner(Node):

    PARAMETERS = {
        'input_dir': str,
        'output_dir': str,
        'targets': dict | str,
        'method': str,
        'dim': int
    }

    def __init__(self, input_dir: str, output_dir: str, targets: dict | str, method: str, dim: int) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else StorageHelper.load_targets(targets)
        self.method = getattr(self, method)
        self.dim = dim

    def run(self) -> None:
        pattern = r'_(\d+)'

        for compound, constituents in self.targets.items():
            compound_input_dir = os.path.join(self.input_dir, compound)
            compound_output_dir = os.path.join(self.output_dir, compound)
            StorageHelper.create_dir(compound_output_dir)

            file_names = StorageHelper.list_files(compound_input_dir)
            for target in [compound] + constituents:
                vectors = []
                for file_name in file_names:
                    file_name_prefix = re.split(pattern, file_name)[0]
                    if target == file_name_prefix:
                        target_file = os.path.join(
                            compound_input_dir, f'{file_name}.pt')
                        vectors.append(StorageHelper.load_vector(target_file))

                stacked_tensor = torch.stack(vectors, dim=0)
                combined_vector = self.method(stacked_tensor, self.dim)
                target_output_file = os.path.join(
                    compound_output_dir, f'{target}_0.pt')
                StorageHelper.save_vector(combined_vector, target_output_file)

    def mean(self, tensor: torch.Tensor, dim: int) -> torch.Tensor:
        return torch.mean(tensor, dim)
