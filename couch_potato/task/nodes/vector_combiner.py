import re

import torch
from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import list_files, load_targets, load_vector, save_vector


class VectorCombiner(Node):

    PARAMETERS = {
        "input_dir": str,
        "output_dir": str,
        "targets": dict | str,
        "method": str,
        "dim": int,
    }

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        targets: dict | str,
        method: str,
        dim: int,
    ) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.method = getattr(self, method)
        self.dim = dim

    def run(self) -> None:
        pattern = r"_(\d+)"

        for compound, constituents in self.targets.items():
            compound_input_dir = join_paths(self.input_dir, compound)
            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)
            file_names = list_files(compound_input_dir, False)

            for target in [compound] + constituents:
                vectors = []
                for file_name in file_names:
                    file_name_prefix = re.split(pattern, file_name)[0]
                    if target == file_name_prefix:
                        file_input_path = join_paths(
                            compound_input_dir, f"{file_name}.pt"
                        )
                        vectors.append(load_vector(file_input_path))

                stacked_tensor = torch.stack(vectors, dim=0)
                combined_vector = self.method(stacked_tensor, self.dim)
                file_output_path = join_paths(compound_output_dir, f"{target}.pt")
                save_vector(combined_vector, file_output_path)

    def mean(self, tensor: torch.Tensor, dim: int) -> torch.Tensor:
        return torch.mean(tensor, dim)

    def max(self, tensor: torch.Tensor, dim: int) -> torch.Tensor:
        return torch.max(tensor, dim)[0]
