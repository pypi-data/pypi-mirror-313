import csv
from datetime import datetime, timedelta, timezone
from wwttoolbox.transformers.swat.cast_functions import str_to_int, str_to_float
import re


class CsvReader:
    """Read SWAT output files in csv format."""

    def __init__(self, csv_path: str, skip_column_length_check: bool = False) -> None:
        """Initialize the CsvReader.

        Parameters:
        - csv_path (str): The path to the csv file.
        """
        self.csv_path = csv_path
        self.skip_column_length_check = skip_column_length_check

        # settings
        self.metadata_index = 0
        self.header_index = 1
        self.units_index = 2
        self.data_index = 3
        self.jday_col_name = "jday"
        self.year_col_name = "yr"
        self.name_col_name = "name"
        self.day_col_name = "day"
        self.month_col_name = "mon"
        self.time_offset = timedelta(hours=12)

        # content
        self.header: list[str] = []
        self.units: dict[str, str] = {}
        self.ordered_data: list[list[str]] = []

    def read_csv(self):
        """Read the CSV file and set the header, units and ordered data attributes."""
        self._read_header()
        self._read_units()
        self._read_data_to_ordered_data()
        self._validate_ordered_data()

    def get_time_dimension(self) -> list[datetime]:
        """Get the time dimension from the ordered data.

        Returns:
        - list[datetime]: The time dimension in utc timezone with the specified time offset.
        """
        time_data = []

        for day_data in self.ordered_data:
            first_gis_unit_row = day_data[0]
            year = int(first_gis_unit_row[self.header.index(self.year_col_name)])
            month = int(first_gis_unit_row[self.header.index(self.month_col_name)])
            day = int(first_gis_unit_row[self.header.index(self.day_col_name)])

            time_data.append(
                datetime(year, month, day, tzinfo=timezone.utc) + self.time_offset
            )

        return time_data

    def get_gis_unit_dimension(self) -> list[int]:
        """Get the gis unit dimension from the ordered data.

        The first day sets the dimensions.

        The unit id is an integer taken from the 'name' column where the specified prefix is removed.

        Returns:
        - list[int]: The gis unit dimension.
        """

        first_day_data = self.ordered_data[0]
        gis_units = []

        for gis_unit in first_day_data:
            name = gis_unit[self.header.index(self.name_col_name)]
            string_value = re.search(r"\d+", name).group()
            numbers = int(string_value)
            gis_units.append(numbers)

        return gis_units

    def get_parameter(self, name: str, dtype: str = "float") -> list[list[int | float]]:
        """Get the parameter from the ordered data.

        Parameters:
        - name (str): The name of the parameter to be extracted.
        - dtype (str): The data type of the parameter. Can be 'int' or 'float'.

        Returns:
        - list[list[int|float]]: The parameter as a list of lists.
        """

        if name not in self.header:
            raise ValueError(f"Parameter {name} not found in the header")

        if dtype == "int":
            cast_func = str_to_int
        elif dtype == "float":
            cast_func = str_to_float
        else:
            raise ValueError(f"dtype must be 'int' or 'float', got {dtype}")

        name_index = self.header.index(name)

        return self._query_parameter(name_index, cast_func)

    def get_col_names(self) -> list[str]:
        """Get the column names from the header.

        The name of the columns are stripped of all spaces.

        Returns:
        - list[str]: The column names.
        """
        return self.header

    def get_units(self) -> dict[str, str]:
        """Get the units from the CSV file.

        The units and names are stripped of all spaces.

        Returns:
        - dict[str, str]: The units as a dictionary with the column names as keys and the units as values.
        """
        return self.units

    ###################################
    # Private methods
    ###################################

    def _query_parameter(
        self, parameter_index: int, cast_func: callable
    ) -> list[list[int | float | None]]:
        """Query the parameter from the ordered data.

        Value that can't be casted are replaced as None.

        Parameters:
        - name (str): The name of the parameter to be extracted.
        - cast_func (callable): The function to cast the parameter to the desired type.

        Returns:
        - list[list[int|float]]: The parameter as a list of lists.
        """
        data = []

        for day_data in self.ordered_data:
            day_values = []
            for gis_unit in day_data:
                day_values.append(cast_func(gis_unit[parameter_index]))
            data.append(day_values)

        return data

    def _read_header(self):
        """Read the header from the CSV file.

        Removes all spaces from the column names.

        The order is kept and no columns are removed.

        Sets the header attribute.
        """
        header_row = self._read_one_row(self.header_index)
        self.header = [column.replace(" ", "") for column in header_row]

    def _read_units(self):
        """Read the units from the CSV file.

        Creates a dictionary with the column names as keys and the units as values.

        All spaces are removed from the units.

        If the unit is empty, empty string is used.
        """
        units_row = self._read_one_row(self.units_index)

        if self.skip_column_length_check:
            print(
                "Skipping check for match between headers and units - missing units will be empty strings"
            )
        else:
            self._validate_row_length(units_row)

        for index, col_name in enumerate(self.header):
            unit = units_row[index].replace(" ", "") if len(units_row) > index else ""
            self.units[col_name] = unit

    def _read_one_row(self, row_index) -> list[str]:
        """Read one row from the CSV file.

        Does not validate or format the row.

        Parameters:
        - row_index (int): The index of the row to be read.

        Returns:
        - list[str] | None: The row as a list of strings, returns None if row out of bounds.
        """
        with open(self.csv_path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            for index, row in enumerate(reader):
                if index == row_index:
                    return row

    def _read_data_to_ordered_data(self):
        """Read the data from the CSV file.

        **Assumes that the data is ordered by jday, year and unit in ascending order.**

        The data is grouped by date.

        All columns are kept and values are not processed.

        Start reading from the data_index attribute.

        Does NOT validate the data.
        """
        jday_index = self.header.index(self.jday_col_name)

        with open(self.csv_path, "r") as f:
            reader = csv.reader(f, delimiter=",")

            day_data = []
            active_jday = None

            for index, row in enumerate(reader):
                # skip rows until data_index
                if index < self.data_index:
                    continue

                # initialize active_jday and active_year
                if index == self.data_index:
                    active_jday = row[jday_index]

                # if jday and year are different from the active ones, append the day_data to the ordered_data and reset
                if row[jday_index] != active_jday:
                    self.ordered_data.append(day_data)
                    day_data = []
                    active_jday = row[jday_index]

                day_data.append(row)

            # append the last day_data
            self.ordered_data.append(day_data)

    ###################################
    # Validators
    ###################################

    def _validate_ordered_data(self):
        """Validate the ordered data.

        The ordered data is valid if following conditions are met:
        - All rows have the same number of columns as the header.
        - The data is ordered by jday and year in ascending order.
        - All days have the same units and ordered in ascending order.

        Raises:
        - ValueError: If the ordered data is not valid.
        """
        # validate the length of the rows
        if self.skip_column_length_check:
            print(
                "Skipping check for number of columns headers matching number of columns in data"
            )
        else:
            self._validate_ordered_data_row_length()

        self._validate_ordered_data_by_date()

        self._validate_ordered_data_gis_units()

    def _validate_row_length(self, row: list[str]):
        """Validate a row from the CSV file.

        The row is valid if it has the same number of columns as the header.

        Parameters:
        - row (list[str]): The row to be validated.

        Raises:
        - ValueError: If the row is not valid.
        """
        if len(row) != len(self.header):
            raise ValueError("Row has different number of columns than header")

    def _validate_ordered_data_row_length(self):
        """Validates that all rows in the ordered data have the same length as the header."""
        header_length = len(self.header)
        for day_row in self.ordered_data:
            for unit_row in day_row:
                if len(unit_row) != header_length:
                    raise ValueError(
                        "Ordered data has different row lengths compared to the header"
                    )

    def _validate_ordered_data_by_date(self):
        """Validates that the ordered data is ordered by date."""
        if len(self.ordered_data) <= 1:
            return

        jday_index = self.header.index(self.jday_col_name)
        year_index = self.header.index(self.year_col_name)

        current_jday = int(self.ordered_data[0][0][jday_index])
        current_year = int(self.ordered_data[0][0][year_index])

        for index, day_data in enumerate(self.ordered_data):
            # Skip the first day, since it is the initial day
            if index == 0:
                continue

            if int(day_data[0][year_index]) == current_year:
                # When it is the same year, the jday should be the next day
                if int(day_data[0][jday_index]) == current_jday + 1:
                    current_jday = int(day_data[0][jday_index])
                else:
                    raise ValueError(
                        "Ordered data is not ordered by date. The jday is not the next day"
                    )
            elif int(day_data[0][year_index]) == current_year + 1:
                # When it is the next year, the jday should be 1
                if int(day_data[0][jday_index]) == 1:
                    current_jday = 1
                    current_year = int(day_data[0][year_index])
                else:
                    raise ValueError(
                        "Ordered data is not ordered by date. The jday is not 1 after the year change"
                    )
            else:
                raise ValueError(
                    "Ordered data is not ordered by date. The year is not the next year"
                )

    def _validate_ordered_data_gis_units(self):
        """Validates that the ordered data has the same gis units for all days in ascending order.

        The first day sets the baseline.

        """
        if len(self.ordered_data) <= 1:
            return

        initial_day_data = self.ordered_data[0]
        initial_day_data_length = len(initial_day_data)

        if not self._validate_gis_unit_lexicographic_order(initial_day_data):
            raise ValueError(
                "Gis units are not in lexicographic order for the first day"
            )

        for index, day_data in enumerate(self.ordered_data):
            # Skip the first day, since it is the initial day
            if index == 0:
                continue

            if len(day_data) != initial_day_data_length:
                raise ValueError(
                    f"Day {index+1} has different number of gis units compared to the first day"
                )

            if not self._validate_gis_unit_lexicographic_order(day_data):
                raise ValueError(
                    f"Gis units are not in lexicographic order for day {index+1}"
                )

    def _validate_gis_unit_lexicographic_order(self, day_data: list[list[str]]) -> bool:
        """Validates that the ordered data has the same gis units for all days in ascending order.

        Compares the order on the 'name' column using lexicographic order.

        The first day sets the baseline.

        """
        name_index = self.header.index(self.name_col_name)

        last_name = ""

        for gis_units in day_data:
            if gis_units[name_index] < last_name:
                return False
            last_name = gis_units[name_index]

        return True
