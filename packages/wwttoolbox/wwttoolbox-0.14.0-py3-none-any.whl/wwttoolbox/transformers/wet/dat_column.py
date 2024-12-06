class DatColumn:
    """Object representing column in a WET .dat file."""

    def __init__(self, col_name: str, format: str, data: list):
        """Initialize DatColumn object.

        Parameters:
        col_name (str): Name of the column.
        format (str): Format of the column.
            - 'date' for datetime object to be formatted as 'YYYY-MM-DD'.
            - 'time' for datetime object to be formatted as 'HH:MM:SS'.
            - '.2f' or similar to format float.
            - "" for default formatting.
        data (list): List of data for the column.
            - Either int, float or datetime object.
        """
        self.col_name = col_name
        self.format = format
        self.data = data
        self.formatted_data = None

    def format_data(self):
        """Format data in column.

        When formatting time, microseconds and timezones are ignored.

        """

        if self.format == "date":
            self.formatted_data = [d.strftime("%Y-%m-%d") for d in self.data]
        elif self.format == "time":
            self.formatted_data = [d.strftime("%H:%M:%S") for d in self.data]
        elif self.format:
            self.formatted_data = [f"{d:{self.format}}" for d in self.data]
        else:
            self.formatted_data = [str(d) for d in self.data]
