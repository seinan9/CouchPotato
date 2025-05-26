from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import load_csv, load_targets, save_csv


class ResultCombiner(Node):

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
