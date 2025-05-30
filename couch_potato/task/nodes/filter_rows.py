from couch_potato.core.node import Node
from couch_potato.task.utils import load_csv, save_csv


class FilterRows(Node):
    """
    Filters `file_to_filter` to only include rows where a value in `match_column`
    matches a value from `filter_column` in `filter_file`. Writes the result to `output_file`.

    Parameters:
        - filter_file (str): CSV file containing values to match.
        - file_to_filter (str): CSV file to be filtered.
        - filter_column_idx (int): Index of the column in `filter_file` to extract match values.
        - match_column_idx (int): Index of the column in `file_to_filter` to check against.
        - output_file (str): File path to save the filtered rows.
    """

    PARAMETERS = {
        "filter_file": str,
        "file_to_filter": str,
        "filter_column": int,
        "match_column": int,
        "output_file": str,
    }

    def __init__(
        self,
        filter_file: str,
        file_to_filter: str,
        filter_column: int,
        match_column: int,
        output_file: str,
    ):
        self.filter_file = filter_file
        self.file_to_filter = file_to_filter
        self.filter_column = filter_column
        self.match_column = match_column
        self.output_file = output_file

    def run(self):
        filter_data = load_csv(self.filter_file)
        data_to_filter = load_csv(self.file_to_filter)

        # Get headers and the relevant column names from indices
        filter_header = list(filter_data[0].keys())
        filter_column = filter_header[self.filter_column]

        filter_values = set(row[filter_column] for row in filter_data)

        filter_target_header = list(data_to_filter[0].keys())
        match_column = filter_target_header[self.match_column]

        # Apply filtering based on extracted values
        filtered_data = [
            row for row in data_to_filter if row[match_column] in filter_values
        ]

        # Save result
        header = list(filtered_data[0].keys())
        save_csv(header, filtered_data, self.output_file)
