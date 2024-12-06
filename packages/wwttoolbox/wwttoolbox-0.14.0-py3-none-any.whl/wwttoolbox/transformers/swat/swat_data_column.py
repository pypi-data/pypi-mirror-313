class SWATDataColumn:
    """Object representing column in a SWAT station data file."""

    def __init__(self, format: str, data: list):
        """Initialize column object.

        Parameters:
        format (str): Format of the column.
            - 'year' for datetime object to be formatted as 'YYYY'.
            - 'day' for datetime object to be formatted as julian day (0-365).
            - 'hour' for datetime object to be formatted as hour of the day (0-23).
            - '.2f' or similar to format float.
            - "" for default formatting.
        data (list): List of data for the column.
            - Either int, float or datetime object.
        """
        self.format = format
        self.data = data

    def format_data(self) -> list[str]:
        """Format data in column.

        When formatting time, microseconds and timezones are ignored.

        Returns:
         - list[str]: Formatted data.
        """

        if self.format == "year":
            return [d.strftime("%Y") for d in self.data]
        elif self.format == "day":
            return [str(d.timetuple().tm_yday) for d in self.data]
        elif self.format == "hour":
            return [str(d.timetuple().tm_hour) for d in self.data]
        elif self.format:
            return [f"{d:{self.format}}" for d in self.data]
        else:
            return [str(d) for d in self.data]
