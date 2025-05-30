from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class SelectTopRows(Node):
    """
    Selects the top N rows from a CSV file.

    Parameters:
        - input_file: Path to the input CSV file
        - num_rows: Number of rows to select from the top
        - output_file: Path to save the selected rows
    """

    PARAMETERS = {
        "input_file": str,
        "num_rows": int,
        "output_file": str,
    }

    def __init__(
        self,
        input_file: str,
        num_rows: int,
        output_file: str,
    ):
        self.input_file = input_file
        self.num_rows = num_rows
        self.output_file = output_file

    def run(self):
        data = load_csv(self.input_file)
        top_n_data = data[: self.num_rows]
        header = list(top_n_data[0].keys())
        save_csv(header, top_n_data, self.output_file)
