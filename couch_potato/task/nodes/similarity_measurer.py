import torch
from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import load_targets, load_vector, save_csv


class SimilarityMeasurer(Node):

    PARAMETERS = {
        "input_dir": str,
        "output_dir": str,
        "targets": str,
        "measure": str,
        "dim": int,
    }

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        targets: dict | str,
        measure: str,
        dim: int,
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.measure = getattr(self, measure)
        self.dim = dim

    def run(self):
        for compound, constituents in self.targets.items():
            compound_input_dir = join_paths(self.input_dir, compound)
            compound_input_file = join_paths(compound_input_dir, f"{compound}.pt")
            compound_vector = load_vector(compound_input_file)
            similarities = {}

            for constituent in constituents:
                constituent_input_file = join_paths(
                    compound_input_dir, f"{constituent}.pt"
                )
                constituent_vector = load_vector(constituent_input_file)
                similarities[constituent] = round(
                    self.measure(compound_vector, constituent_vector, self.dim), 3
                )

            compound_output_dir = join_paths(self.output_dir, compound)
            compound_output_file = join_paths(compound_output_dir, "similarities.csv")
            create_dir(compound_output_dir)

            csv_header = ["compound", "sim_const_1", "sim_const_2"]
            csv_values = [
                {
                    "compound": compound,
                    "sim_const_1": similarities[constituents[0]],
                    "sim_const_2": similarities[constituents[1]],
                }
            ]
            save_csv(csv_header, csv_values, compound_output_file)

    def cosine(self, vector0: torch.Tensor, vector1: torch.Tensor, dim: int) -> float:
        return torch.cosine_similarity(vector0, vector1, dim).item()
