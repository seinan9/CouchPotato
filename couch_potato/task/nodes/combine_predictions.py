from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class CombinePredictions(Node):

    PARAMETERS = {
        "input_0": str,
        "input_1": str,
        "weight": float,
        "output_file": str,
    }

    def __init__(
        self, input_0: str, input_1: str, weight: float, output_file: str
    ) -> None:
        self.input_0 = input_0
        self.input_1 = input_1
        self.weight = weight
        self.output_file = output_file

    def run(self):
        data_0 = load_csv(self.input_0)
        data_1 = load_csv(self.input_1)

        header = list(data_0[0].keys())
        key_field = header[0]
        value_fields = header[1:]

        combined = []
        for row0, row1 in zip(data_0, data_1):

            combined_row = {key_field: row0[key_field]}
            for field in value_fields:
                val0 = float(row0[field])
                val1 = float(row1[field])
                combined_val = round(self.weight * val0 + (1 - self.weight) * val1, 3)
                combined_row[field] = combined_val

            combined.append(combined_row)

        save_csv(header, combined, self.output_file)
