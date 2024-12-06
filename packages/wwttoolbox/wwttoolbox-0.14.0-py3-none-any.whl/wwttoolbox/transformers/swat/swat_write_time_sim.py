from datetime import datetime, timedelta
import csv


class SWATWriteTimeSim:
    """Generate the time.sim file for the swat model."""

    def __init__(self, file_path: str, start_date: datetime, end_date: datetime):
        """Initialize the class

        Parameters:
        - file_path (str): Path where to save the file.
        - start_date (datetime): Start date of the simulation.
        - end_date (datetime): End date of the simulation.
        """
        self.file_path = file_path
        self.start_date = start_date
        self.end_date = end_date

    def write(self):
        """Write the data to the file."""
        start_year, start_day = self._get_year_and_days(self.start_date)
        end_year, end_day = self._get_year_and_days(self.end_date)

        lines = []
        lines.append(["SWAT time.sim file"])
        lines.append(["day_start", "yrc_start", "day_end", "yrc_end", "step"])
        lines.append([start_day, start_year, end_day, end_year, "0"])

        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file, delimiter=" ")
            writer.writerows(lines)

    def _get_year_and_days(self, date: datetime) -> tuple:
        """Get the year and day of the year for a date.

        Parameters:
        - date (datetime): Date to get the year and day of the year.

        Returns:
        - year (str): Year of the date.
        - day (str): Day of the year of the date.
        """
        year = str(date.year)
        day = str(date.timetuple().tm_yday)
        return year, day
