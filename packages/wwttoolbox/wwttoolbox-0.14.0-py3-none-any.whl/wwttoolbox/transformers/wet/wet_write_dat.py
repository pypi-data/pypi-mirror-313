from .dat_column import DatColumn
import csv


class WetWriteDat:
    """Write data to a WET .dat file."""

    def __init__(self, file_path, include_header=True, use_tab_delimiter=False):
        self.file_path = file_path
        self.include_header = include_header
        self.use_tab_delimiter = use_tab_delimiter
        self.cols: list[DatColumn] = []

    def add_column(self, col_name: str, format: str, data: list):
        """Add column to the .dat file.

        The order the columns are added is the order they will be written to the file.

        Parameters:
        col_name (str): Name of the column.
        format (str): Format of the column.
            - 'date' for datetime object to be formatted as 'YYYY-MM-DD'.
            - 'time' for datetime object to be formatted as 'HH:MM:SS'.
            - '.2f' or similar to format float.
            - "" for default formatting.
        data (list): List of data for the column.
            - Either int, float or datetime object
        """

        self.cols.append(DatColumn(col_name, format, data))

    def format_data(self):
        """Format data in each columns.

        Must be called before writing to file.
        """

        for col in self.cols:
            col.format_data()

    def construct_header(self) -> list[str]:
        """Construct header for the .dat file."""
        headers = []

        for index, col in enumerate(self.cols):
            formatted_col_name = col.col_name.replace(" ", "_")
            if index == 0:
                headers.append(f"!{formatted_col_name}")
            else:
                headers.append(formatted_col_name)

        return headers

    def write(self):
        """Writes the data to the .dat file."""
        delimiter = " " if not self.use_tab_delimiter else "\t"

        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=delimiter)

            if self.include_header:
                writer.writerow(self.construct_header())

            for row in zip(*[col.formatted_data for col in self.cols]):
                writer.writerow(row)
