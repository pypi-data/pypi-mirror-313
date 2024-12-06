from wwttoolbox.transformers.swat.csv_reader import CsvReader
from wwttoolbox.nc import NCTool


class Csv2NetcdfNoGisDim:

    def __init__(self, csv_reader: CsvReader, netcdf_path: str, parameters: list[str]):
        """Instantiates a Csv2NetcdfNoGisDim object.

        Parameters:
        - csv_reader (CsvReader): The CsvReader loaded with the csv file.
        - netcdf_path (str): The path to the NetCDF file.
        - parameters (list[str]): The parameters to write to the NetCDF file. If empty all parameters will be written.
        """
        self.netcdf_path: str = netcdf_path
        self.csv_reader = csv_reader
        self.parameters: list[str] = parameters

    def transform(self):
        """Transforms the CSV file to a NetCDF file."""
        self.load_csv()
        self.set_parameters_to_write()
        self.create_netcdf()
        self.write_parameters()

    def load_csv(self):
        """Loads the CSV file into memory."""
        self.csv_reader.read_csv()

    def set_parameters_to_write(self):
        """Sets the parameters to write to the NetCDF file.

        If no parameters are provided, all parameters will be written.

        """

        if len(self.parameters) > 0:
            return

        col_names = self.csv_reader.get_col_names()

        for col_name in col_names:
            if col_name in [
                "jday",
                "mon",
                "day",
                "yr",
                "unit",
                "gis_id",
                "name",
                "null",
            ]:
                continue
            self.parameters.append(col_name)

    def create_netcdf(self):
        """Creates the NetCDF file."""

        time_data = self.csv_reader.get_time_dimension()

        with NCTool(self.netcdf_path, "w") as tool:
            tool.add_time_dimension()
            tool.add_time_variable()
            tool.write_time_data(time_data)

    def write_parameters(self):
        """Writes the parameters to the NetCDF file."""

        for parameter in self.parameters:
            data2d = self.csv_reader.get_parameter(parameter, "float")
            unit = self.csv_reader.get_units()[parameter]
            data1d = self._transform_to_single_dim(data2d)

            with NCTool(self.netcdf_path, "a") as tool:
                tool.add_variable(parameter, "float", ["time"])
                tool.add_variable_attribute(parameter, "units", unit)
                tool.write_data(parameter, data1d)

    def _transform_to_single_dim(
        self, data: list[list[int | float]]
    ) -> list[int | float]:
        """Transforms a 2D list to a 1D list."""
        return [sublist[0] for sublist in data]
