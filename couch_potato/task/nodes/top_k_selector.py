from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class TopKSelector(Node):

    PARAMETERS = {
        "input_file": str,
        "output_file": str,
        "top_k": int,
    }

    def __init__(
        self,
        input_file: str,
        output_file: str,
        top_k: int,
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.top_k = top_k

    def run(self):
        data = load_csv(self.input_file)
        top_k_data = data[: self.top_k]
        header = list(top_k_data[0].keys())
        save_csv(header, top_k_data, self.output_file)
