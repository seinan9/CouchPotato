from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import load_csv, save_csv
from scipy.stats import spearmanr


class CorrelationCalculator(Node):
    """
    Node to compute correlation between selected columns of two CSV files.

    This node loads two datasets, selects specified columns by index,
    computes correlation scores (e.g., Spearman), and saves the results
    in a CSV file. Each correlation is labeled as corr_1, corr_2, etc.

    Parameters:
        - input_file_0: Path to the first CSV file
        - input_file_1: Path to the second CSV file
        - columns_0: List of column indices from the first file
        - columns_1: List of column indices from the second file
        - output_dir: Directory to save the correlation results
        - measure: Correlation measure to use (currently supports 'spearman')
    """

    PARAMETERS = {
        "input_file_0": str,
        "input_file_1": str,
        "columns_0": list,
        "columns_1": list,
        "output_dir": str,
        "measure": str,
    }

    def __init__(
        self,
        input_file_0: str,
        input_file_1: str,
        columns_0: list,
        columns_1: list,
        output_dir: str,
        measure: str,
    ) -> None:
        if len(columns_0) != len(columns_1):
            raise ValueError("Mismatched lengths between columns.")

        # Load data from both input files
        self.data_0 = load_csv(input_file_0)
        self.data_1 = load_csv(input_file_1)

        # Map column indices to header names and pair them
        header_0 = list(self.data_0[0].keys())
        header_1 = list(self.data_1[0].keys())
        self.header_pairs = list(
            zip(
                [header_0[i] for i in columns_0],
                [header_1[i] for i in columns_1],
            )
        )

        self.output_dir = output_dir
        create_dir(output_dir)

        # Resolve the correlation method (e.g., spearman)
        try:
            self.measure = getattr(self, measure)
        except AttributeError:
            raise ValueError(f"Unknown correlation measure: {measure}")

    def run(self) -> None:
        correlations = {}
        # Compute correlation for each column pair
        for i, (col0, col1) in enumerate(self.header_pairs):
            values_0 = [row[col0] for row in self.data_0]
            values_1 = [row[col1] for row in self.data_1]
            correlation = round(self.measure(values_0, values_1), 3)
            correlations[f"corr_{i+1}"] = correlation

        # Save results to a CSV file
        output_file = join_paths(self.output_dir, "correlations.csv")
        save_csv(list(correlations.keys()), [correlations], output_file)

    def spearman(self, values_0: list, values_1: list) -> float:
        correlation, _ = spearmanr(values_0, values_1)
        return correlation
