from pathlib import Path

from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, load_targets, save_csv


class AggregateResults(Node):
    """
    Node to aggregate CSV result files for each compound into a single combined CSV.

    Parameters:
        - input_dir: Directory containing per-compound result subfolders.
        - file_name: Name of the CSV file to load from each compound's subdirectory.
        - targets: Dictionary or path to YAML file mapping compounds to constituents.
        - output_file: File where the combined results will be saved.
    """

    PARAMETERS = {
        "input_dir": str,
        "file_name": str,
        "targets": dict | str,
        "output_file": str,
    }

    def __init__(
        self, input_dir: str, file_name: str, targets: dict | str, output_file: str
    ) -> None:
        self.input_dir = Path(input_dir)
        self.file_name = file_name
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.output_file = output_file

    def run(self):
        data = []

        for compound in self.targets.keys():
            compound_input_file_path = self.input_dir / compound / self.file_name
            data.append(*load_csv(compound_input_file_path))

        header = [key for key in data[0].keys()]

        save_csv(header, data, self.output_file)
