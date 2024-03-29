from node import Node
from utils import Utils
from helpers.storage_helper import StorageHelper


class ResultCombiner(Node):

    PARAMETERS = {
        'input_dir': str,
        'output_dir': str,
        'targets': dict | str,
        'file_name': str
    }

    def __init__(self, input_dir: str, output_dir: str, targets: dict | str, file_name: str) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else StorageHelper.load_targets(targets)
        self.file_name = file_name
        Utils.create_dir(self.output_dir)

    def run(self):
        data = []

        for compound in self.targets.keys():
            compound_input_file_path = Utils.join_paths(
                self.input_dir, compound, self.file_name)
            data.append(*StorageHelper.load_csv(compound_input_file_path))

        header = [key for key in data[0].keys()]
        output_file_path = Utils.join_paths(self.output_dir, self.file_name)
        StorageHelper.save_csv(header, data, output_file_path)
