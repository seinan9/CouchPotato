from pathlib import Path

from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class PredictionCombiner(Node):

    PARAMETERS = {
        "input_file_0": str,
        "input_file_1": str,
        "weight": float,
        "output_dir": str,
    }

    def __init__(
        self, input_file_0: str, input_file_1: str, weight: float, output_dir: str
    ) -> None:
        self.input_file_0 = input_file_0
        self.input_file_1 = input_file_1
        self.weight = weight
        self.output_dir = Path(output_dir)

    def run(self):
        data_0 = load_csv(self.input_file_0)
        data_1 = load_csv(self.input_file_1)

        if len(data_0) != len(data_1):
            raise ValueError("Input files must have the same number of rows.")

        header = list(data_0[0].keys())
        key_field = header[0]
        value_fields = header[1:]

        combined = []
        for row0, row1 in zip(data_0, data_1):
            if row0[key_field] != row1[key_field]:
                raise ValueError(
                    f"Mismatched compound names: {row0[key_field]} vs {row1[key_field]}"
                )

            combined_row = {key_field: row0[key_field]}
            for field in value_fields:
                val0 = float(row0[field])
                val1 = float(row1[field])
                combined_val = round(self.weight * val0 + (1 - self.weight) * val1, 3)
                combined_row[field] = combined_val

            combined.append(combined_row)

        output_file = self.output_dir / "weighted.csv"
        save_csv(header, combined, output_file)
