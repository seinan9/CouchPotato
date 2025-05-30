from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class Sorter(Node):

    PARAMETERS = {
        "input_file": str,
        "output_file": str,
        "column": int,
        "ascending": bool,
    }

    def __init__(
        self,
        input_file: str,
        output_file: str,
        column: int,
        ascending: bool,
    ):
        self.input_file = input_file
        self.column = column
        self.ascending = ascending
        self.output_file = output_file

    def run(self):
        data = load_csv(self.input_file)

        sorted_data = sorted(
            data, key=lambda x: float(x[self.column]), reverse=not self.ascending
        )

        header = list(sorted_data[0].keys())
        save_csv(header, sorted_data, self.output_file)
