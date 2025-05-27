from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import load_csv, load_targets, save_csv


class ResultCombiner(Node):
    """
    Node to aggregate CSV result files for each compound into a single combined CSV.

    Parameters:
        - input_dir: Directory containing per-compound result subfolders.
        - output_dir: Directory where the combined result file will be saved.
        - targets: Dictionary or path to YAML file mapping compounds to constituents.
        - file_name: Name of the CSV file to load from each compound's subdirectory.
    """

    PARAMETERS = {
        "input_dir": str,
        "output_dir": str,
        "targets": dict | str,
        "file_name": str,
    }

    def __init__(
        self, input_dir: str, output_dir: str, targets: dict | str, file_name: str
    ) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.file_name = file_name
        create_dir(self.output_dir)

    def run(self):
        data = []

        for compound in self.targets.keys():
            compound_input_file_path = join_paths(
                self.input_dir, compound, self.file_name
            )
            data.append(*load_csv(compound_input_file_path))

        header = [key for key in data[0].keys()]

        output_file_path = join_paths(self.output_dir, self.file_name)
        save_csv(header, data, output_file_path)
