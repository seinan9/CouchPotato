from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv
from scipy.stats import spearmanr


class Correlate(Node):
    """
    Node to compute correlation between selected columns of two CSV files.

    This node loads two datasets, selects specified columns by index,
    computes correlation scores (e.g., Spearman), and saves the results
    in a CSV file. Each correlation is labeled as corr_1, corr_2, etc.

    Parameters:
        - input_0: Path to the first CSV file
        - input_1: Path to the second CSV file
        - columns_0: List of column indices from the first file
        - columns_1: List of column indices from the second file
        - output_dir: Directory to save the correlation results
        - measure: Correlation measure to use (currently supports 'spearman')
    """

    PARAMETERS = {
        "input_0": str,
        "input_1": str,
        "columns_0": list,
        "columns_1": list,
        "measure": str,
        "output_file": str,
    }

    def __init__(
        self,
        input_0: str,
        input_1: str,
        columns_0: list,
        columns_1: list,
        measure: str,
        output_file: str,
    ) -> None:
        self.input_0 = input_0
        self.input_1 = input_1
        self.columns_0 = columns_0
        self.columns_1 = columns_1
        self.measure = getattr(self, measure)
        self.output_file = output_file

    def run(self) -> None:
        # Load data
        data_0 = load_csv(self.input_0)
        data_1 = load_csv(self.input_1)

        # Identify and pair headers
        header_0 = list(data_0[0].keys())
        header_1 = list(data_1[0].keys())
        header_pairs = list(
            zip(
                [header_0[i] for i in self.columns_0],
                [header_1[i] for i in self.columns_1],
            )
        )

        correlations = {}

        # Compute correlation for each column pair
        for i, (col0, col1) in enumerate(header_pairs):
            values_0 = [row[col0] for row in data_0]
            values_1 = [row[col1] for row in data_1]
            correlation = round(self.measure(values_0, values_1), 3)
            correlations[f"corr_{i+1}"] = correlation

        # Save results to a CSV file
        save_csv(list(correlations.keys()), [correlations], self.output_file)

    def spearman(self, values_0: list, values_1: list) -> float:
        correlation, _ = spearmanr(values_0, values_1)
        return correlation
