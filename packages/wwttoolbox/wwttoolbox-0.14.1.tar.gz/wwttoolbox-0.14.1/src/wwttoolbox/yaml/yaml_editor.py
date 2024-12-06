from ruamel.yaml import YAML
from datetime import datetime


class YamlEditor:

    def __init__(self):
        self.yaml = YAML()
        self.data: dict = None

    def load(self, path) -> None:
        with open(path, "r") as f:
            # self.yaml.version = (1, 1)
            self.data = self.yaml.load(f)

        if self.data is None:
            self.data = {}

    def save(self, path) -> None:
        with open(path, "w") as f:
            # self.yaml.default_style = None
            # self.yaml.default_flow_style = False
            self.yaml.dump(self.data, f)

    def set_int(self, path: str, value: int) -> None:
        """Write an integer value to the YAML file at the given path.

        Existing value on the path will be overwritten.

        Parameters:
        - path (str): The path to the value specified by '/' e.g. "nested/another"
        - value (int): The integer value to write to the YAML file

        Returns:
        - None

        Raises:
        - ValueError: If the value is not an integer
        """

        if type(value) != int:
            raise ValueError(f"Value must be an integer, got {type(value)}")

        parsed_path = self._parse_path(path)
        self.data = self._apply_value(parsed_path, value, self.data)

    def set_float(self, path: str, value: float, format: str = None) -> None:
        """Write a float value to the YAML file at the given path.

        Existing value on the path will be overwritten.

        Parameters:
        - path (str): The path to the value specified by '/' e.g. "nested/another"
        - value (float): The float value to write to the YAML file
        - format (str): The format to write the float value in, e.g. ".2f", if not provided the full float value will be written

        Returns:
        - None

        Raises:
        - ValueError: If the value is not a float
        """

        if type(value) != float:
            raise ValueError(f"Value must be a float, got {type(value)}")

        if format:
            value_str = f"{value:{format}}"
            value = float(value_str)

        parsed_path = self._parse_path(path)
        self.data = self._apply_value(parsed_path, value, self.data)

    def set_string(self, path: str, value: str) -> None:
        """Write a string value to the YAML file at the given path.

        Existing value on the path will be overwritten.

        Parameters:
        - path (str): The path to the value specified by '/' e.g. "nested/another"
        - value (str): The string value to write to the YAML file

        Returns:
        - None

        Raises:
        - ValueError: If the value is not a string
        """

        if type(value) != str:
            raise ValueError(f"Value must be a string, got {type(value)}")

        parsed_path = self._parse_path(path)
        self.data = self._apply_value(parsed_path, value, self.data)

    def set_datetime_no_quotes(self, path: str, value: datetime) -> None:
        """Write a datetime without quotes to the YAML file at the given path.

        Existing value on the path will be overwritten.

        The datetime value will be written in the format "YYYY-MM-DD HH:MM:SS".

        Parameters:
        - path (str): The path to the value specified by '/' e.g. "nested/another"
        - value (datetime): The datetime value to write to the YAML file

        Returns:
        - None

        Raises:
        - ValueError: If the value is not a datetime
        """

        if type(value) != datetime:
            raise ValueError(f"Value must be a datetime, got {type(value)}")

        value_copy = value.replace(microsecond=0, tzinfo=None)

        parsed_path = self._parse_path(path)
        self.data = self._apply_value(parsed_path, value_copy, self.data)

    def set_datetime(
        self, path: str, value: datetime, format: str = "%Y-%m-%d %H:%M:%S"
    ) -> None:
        """Write a datetime value to the YAML file at the given path.

        **Warning**: This will most likely apply quotes around the timestamp value.

        Existing value on the path will be overwritten.

        Any timezone information will be lost when writing the datetime value.

        Parameters:
        - path (str): The path to the value specified by '/' e.g. "nested/another"
        - value (datetime): The datetime value to write to the YAML file
        - format (str): The format to write the datetime value in, e.g. "%Y-%m-%d %H:%M:%S"
          - Default: "%Y-%m-%d %H:%M:%S"

        Returns:
        - None

        Raises:
        - ValueError: If the value is not a datetime

        """

        if type(value) != datetime:
            raise ValueError(f"Value must be a datetime, got {type(value)}")

        value_str = value.strftime(format)
        parsed_path = self._parse_path(path)
        self.data = self._apply_value(parsed_path, value_str, self.data)

    def _parse_path(self, path: str) -> list[str]:
        """Parse the path string into a list of keys."""
        return path.split("/")

    def _apply_value(self, path: list[str], value: any, data: dict) -> dict:
        """Recursively apply the value to the data at the given path."""
        key = path.pop(0)

        if len(path) == 0:
            data[key] = value
            return data

        next_data = data.get(key, {})
        data[key] = self._apply_value(path, value, next_data)

        return data
