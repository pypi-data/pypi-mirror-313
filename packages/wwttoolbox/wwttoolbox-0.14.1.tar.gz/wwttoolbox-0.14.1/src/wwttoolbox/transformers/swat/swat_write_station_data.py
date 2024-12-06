from datetime import datetime
from wwttoolbox.transformers.swat.swat_data_column import SWATDataColumn
import csv


class SWATWriteStationData:
    """Class to generate a SWAT station data file like .pcp or .tem"""

    def __init__(
        self,
        file_path: str,
        lat: float,
        lon: float,
        elev: float,
        isHourly: bool = False,
    ):
        """Initialize the class

        Parameters:
        - file_path (str): Path whereto save the file.
        - lat (float): Latitude of the station.
        - lon (float): Longitude of the station.
        - elev (float): Elevation of the station.
        - isHourly (bool): If the data is hourly. Default is False meaning daily.

        The name of the file will be the station name with the extension of the type.
        """
        self.file_path = file_path
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.isHourly = isHourly
        self.data_columns = []

    def add_time(self, times: list[datetime]):
        """Add a time series to the file.

        Parameters:
        - data (list): List of data for the time series.
        """
        year_col = SWATDataColumn("year", times)
        self.year_col = year_col.format_data()

        day_col = SWATDataColumn("day", times)
        self.day_col = day_col.format_data()

        if self.isHourly:
            hour_col = SWATDataColumn("hour", times)
            self.hour_col = hour_col.format_data()

        self.total_years = str((times[-1].year - times[0].year) + 1)

    def add_column(self, format: str, data: list):
        """Add a column to the file.

        Parameters:
        - col_name (str): Name of the column.
        - data (list): List of data for the column.
        """
        data_col = SWATDataColumn(format, data)
        self.data_columns.append(data_col.format_data())

    def write(self):
        """Write the data to the file."""
        header_lines = self._get_header_lines()
        data_rows = self._get_data_rows()

        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=" ")

            # Write the header lines
            for lines in header_lines:
                writer.writerow(lines)

            for row in data_rows:
                writer.writerow(row)

    def _get_header_lines(self) -> list[str]:
        """Return the header lines of the file.

        The header is the first three lines of the file:
        - Line 1: Generic description of the file.
        - Line 2: Labels for station meta data.
        - Line 3: Values for of the meta data.
        """
        lines = []
        tstep = "0" if self.isHourly == False else "24"

        lines.append(["SWAT station data file"])
        lines.append(["nbyr", "tstep", "lat", "lon", "elev"])
        lines.append(
            [
                self.total_years,
                tstep,
                f"{self.lat:.4f}",
                f"{self.lon:.4f}",
                f"{self.elev:.4f}",
            ]
        )

        return lines

    def _get_data_rows(self) -> list[tuple]:
        """Returns the values for each row in the data file."""

        columns = []
        columns.append(self.year_col)
        columns.append(self.day_col)
        if self.isHourly:
            columns.append(self.hour_col)
        columns.extend(self.data_columns)

        return zip(*columns)
