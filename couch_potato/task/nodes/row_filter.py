from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class RowFilter(Node):
    """
    Filters `file_to_filter` to only include rows where `match_column` matches
    a value in `filter_column` from `filter_file`. Writes the result to `output_file`.

    Args:
        filter_file (str): Path to the CSV file providing values to match.
        filter_column (str): Column name in `filter_file` to use for matching.
        file_to_filter (str): Path to the CSV file that will be filtered.
        match_column (str): Column name in `file_to_filter` to match against filter values.
        output_file (str): Path to save the filtered CSV.
    """

    PARAMETERS = {
        "filter_file": str,
        "filter_column": str,
        "file_to_filter": str,
        "match_column": str,
        "output_file": str,
    }

    def __init__(
        self,
        filter_file: str,
        filter_column: str,
        file_to_filter: str,
        match_column: str,
        output_file: str,
    ):
        self.filter_file = filter_file
        self.filter_column = filter_column
        self.file_to_filter = file_to_filter
        self.match_column = match_column
        self.output_file = output_file

    def run(self):
        # Load data
        filter_data = load_csv(self.filter_file)
        data_to_filter = load_csv(self.file_to_filter)

        # Extract set of allowed values from the filter column
        allowed_values = set(row[self.filter_column] for row in filter_data)

        # Filter rows where match_column matches one of the allowed values
        filtered_data = [
            row for row in data_to_filter if row[self.match_column] in allowed_values
        ]

        # Save result
        header = list(filtered_data[0].keys())
        save_csv(header, filtered_data, self.output_file)
