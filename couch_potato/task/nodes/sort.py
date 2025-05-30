from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class Sort(Node):
    """
    Sorts a CSV file by a specified column (given as index) and writes the result.

    Parameters:
        - input_file: Path to the input CSV file
        - column: Index of the column to sort by (0-based)
        - ascending: Whether to sort in ascending order
        - output_file: Path to save the sorted CSV
    """

    PARAMETERS = {
        "input_file": str,
        "column": int,
        "ascending": bool,
        "output_file": str,
    }

    def __init__(
        self,
        input_file: str,
        column: int,
        ascending: bool,
        output_file: str,
    ):
        self.input_file = input_file
        self.column = column
        self.ascending = ascending
        self.output_file = output_file

    def run(self):
        data = load_csv(self.input_file)
        header = list(data[0].keys())
        column_name = header[self.column]

        # Sort data by specified column
        sorted_data = sorted(
            data, key=lambda row: float(row[column_name]), reverse=not self.ascending
        )

        save_csv(header, sorted_data, self.output_file)
