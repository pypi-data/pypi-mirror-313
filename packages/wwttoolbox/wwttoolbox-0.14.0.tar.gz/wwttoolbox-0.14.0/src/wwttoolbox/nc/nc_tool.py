from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num, date2index
import numpy as np

from .nc_mask_utils import fit_mask_to_shape, get_combined_mask

from .nc_utils import (
    convert_simple_dtype_to_nc_dtype,
    convert_nc_dtype_to_simple_dtype,
    get_related_missing_value_to_simple_dtype,
    convert_none_to_missing_value,
    real_datetimes_to_datetimes,
)


class NCTool:
    """Tool to read and write netCDF files."""

    def __init__(self, path: str, mode: str) -> None:
        """Initializes the NCTool object with a file path and mode.

        Parameters:
        - path (str): The file path to the netCDF file to be opened.
        - mode (str): The mode in which to open the file. Valid modes are 'r' for read,
                    'w' for write (overwrites existing file), and 'a' for append.

        Raises:
        - ValueError: If an invalid mode is provided.
        """

        self.path: str = path
        self.nc: Dataset = None
        self.mode: str = None
        self.masks: dict = None
        self.__set_mode(mode)

    def __enter__(self):
        self.nc = Dataset(self.path, self.mode)
        return self

    def __exit__(self, *args):
        if self.nc:
            self.nc.close()

    def __set_mode(self, mode: str) -> None:
        if mode == "r" or mode == "w" or mode == "a":
            self.mode = mode
        else:
            raise ValueError("Invalid mode. Please use 'r', 'w', or 'a'.")

    #####################################
    # Dimension methods
    #####################################

    def add_time_dimension(self):
        """Adds a time dimension to the netCDF file.

        Will be given a size of UNLIMITED and the name 'time'

        Raises:
        - ValueError: If the dimension already exists in the file.
        """

        if "time" in self.nc.dimensions:
            raise ValueError("Dimension 'time' already exists in the file.")
        else:
            self.nc.createDimension("time", None)

    def add_dimension(self, dim_name: str, size: int) -> None:
        """Adds a dimension to the netCDF file.

        Parameters:
        - dim_name (str): The name of the dimension to be added.
        - size (int): The size of the dimension to be added.

        Raises:
        - ValueError: If the dimension already exists in the file.
        """

        if dim_name in self.nc.dimensions:
            raise ValueError("Dimension already exists in the file.")
        else:
            self.nc.createDimension(dim_name, size)

    def get_all_dimensions(self) -> list:
        """Returns a list of all dimensions in the netCDF file.

        Returns:
        - list: A list of dimension names in the netCDF file.
        """

        return list(self.nc.dimensions.keys())

    def get_queryable_dimensions(self) -> list:
        """Returns a list of dimensions that can be used to query the data.

        Single value dimensions are not queryable.
        Returns:
        - list: A list of dimension names that can be used to query the data.
        """
        return [
            dim
            for dim in self.nc.dimensions
            if len(self.nc.dimensions[dim]) > 1 or self.nc.dimensions[dim].isunlimited()
        ]

    ###################################
    # methods for variables
    ###################################

    def add_time_variable(self):
        """Adds a time variable to the netCDF file.

        Expects the time dimension to be present in the file and the time variable will only have the time dimension.

        Creates a variable capable of storing time data as 64-bit floating point values.

        Time is represented as seconds since the epoch, which is added to the attributes following the CF conventions.
        """

        if "time" in self.nc.variables:
            raise ValueError("Variable already exists in the file.")
        else:
            time_var = self.nc.createVariable("time", "f8", ("time",))
            time_var.setncattr("long_name", "time")
            time_var.setncattr("standard_name", "time")
            time_var.setncattr("units", "seconds since 1970-01-01 00:00:00")
            time_var.setncattr("calendar", "gregorian")

    def add_scalar_variable(self, name: str, dtype: str):
        """Adds a scalar variable to the netCDF file.

        Parameters:
        - name (str): The name of the variable to be added.
        - dtype (str): The data type of the variable to be added.

        dType options:
        - int: 16-bit integer (i2)
        - long: 32-bit integer (i4)
        - float: 32-bit floating point (f4)
        - double: 64-bit floating point (f8)

        Raises:
        - ValueError: If the variable already exists in the file.
        """

        if name in self.nc.variables:
            raise ValueError("Variable already exists in the file.")
        else:
            converted_dtype = convert_simple_dtype_to_nc_dtype(dtype)
            self.nc.createVariable(name, converted_dtype)

    def add_variable(self, name: str, dtype: str, dimensions: list[str]):
        """Adds a variable to the netCDF file.

        Parameters:
        - name (str): The name of the variable to be added.
        - dtype (str): The data type of the variable to be added.
        - dimensions (list[str]): A list of dimension names to associate with the variable, add the unlimited first.
            - Will be convert to tuple: e.g ["time", "depth"] -> ("time", "depth") or ["time"] -> ("time",)

        dType options:
        - int: 16-bit integer (i2)
        - long: 32-bit integer (i4)
        - float: 32-bit floating point (f4)
        - double: 64-bit floating point (f8)

        By default, it will add the missing_value attribute to the variable with the appropriate value based on the data type.

        Unless:
        - If the variable is a coordinate variable, mean a dimension with same name exists

        Raises:
        - ValueError: If the variable already exists in the file.
        """

        if name in self.nc.variables:
            raise ValueError("Variable already exists in the file.")

        converted_dtype = convert_simple_dtype_to_nc_dtype(dtype)
        dimensions_t = tuple(dimensions)
        variable = self.nc.createVariable(name, converted_dtype, dimensions_t)

        if self.is_coordinate_variable(name):
            return

        missing_value = get_related_missing_value_to_simple_dtype(dtype)
        variable.setncattr("missing_value", missing_value)

    def get_all_variables(self) -> list:
        """Returns a list of all variables in the netCDF file.

        Returns:
        - list: A list of variable names in the netCDF file.
        """

        return list(self.nc.variables.keys())

    def get_variable_metadata(self, variable_name: str) -> dict:
        """Returns metadata for a variable in the netCDF file.

        Parameters:
        - variable_name (str): The name of the variable to get metadata for.

        Returns a dict with following keys:
        - variable_name (str): The name of the variable.
        - dimensions (list): A list of dimensions associated with the variable.
        - simple_dtype (str): The simple data type of the variable.
        - nc_dtype (str): The data type of the variable.
        - attributes (dict): A dictionary of attributes associated with the variable.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        return {
            "variable_name": variable_name,
            "dimensions": list(self.nc.variables[variable_name].dimensions),
            "simple_dtype": convert_nc_dtype_to_simple_dtype(
                self.nc.variables[variable_name].dtype
            ),
            "nc_dtype": self.nc.variables[variable_name].dtype,
            "attributes": self.nc.variables[variable_name].__dict__,
        }

    def get_variable_dimensions(self, variable_name: str) -> tuple[str]:
        """Returns the dimensions associated with a variable in the netCDF file.

        Parameters:
        - variable_name (str): The name of the variable to get dimensions for.

        Returns:
        - tuple: A tuple of dimensions associated with the variable in the order the dimensions are applied.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        return self.nc.variables[variable_name].dimensions

    def is_coordinate_variable(self, variable_name: str) -> bool:
        """Checks if the variable is a coordinate variable.

        A coordinate variable is a variable that has the same name as a dimension.

        Parameters:
        - variable_name (str): The name of the variable to check.

        Returns:
        - bool: True if the variable is a coordinate variable, False otherwise.
        """

        return variable_name in self.nc.dimensions.keys()

    ###################################
    # methods for attributes
    ###################################

    def add_global_attribute(
        self, name: str, value: str | int | float | list[str | int | float]
    ):
        """Adds a global attribute to the netCDF file.

        If the attribute already exists, it will be overwritten.

        Parameters:
        - name (str): The name of the attribute to be added.
        - value (str|int|float|list[str|int|float]): The value of the attribute to be added.
        """

        self.nc.setncattr(name, value)

    def add_variable_attribute(
        self,
        variable_name,
        name: str,
        value: str | int | float | list[str | int | float],
    ):
        """Adds an attribute to a variable in the netCDF file.

        If the attribute already exists, it will be overwritten.

        Parameters:
        - variable_name (str): The name of the variable to which the attribute will be added.
        - name (str): The name of the attribute to be added.
        - value (str|int|float|list[str|int|float]): The value of the attribute to be added.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        self.nc.variables[variable_name].setncattr(name, value)

    def get_global_attribute(
        self, name: str
    ) -> str | int | float | list[str | int | float]:
        """Returns the value of a global attribute in the netCDF file.

        Parameters:
        - name (str): The name of the attribute to get the value for.

        Returns:
        - str|int|float|list[str|int|float]: The value of the attribute.

        """

        return self.nc.getncattr(name)

    def get_variable_attribute(
        self, variable_name: str, attribute_name: str
    ) -> str | int | float | list[str | int | float]:
        """Returns the value of an attribute for a variable in the netCDF file.

        Parameters:
        - variable_name (str): The name of the variable to get the attribute value for.
        - attribute_name (str): The name of the attribute to get the value for.

        Returns:
        - str|int|float|list[str|int|float]: The value of the attribute.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        return self.nc.variables[variable_name].getncattr(attribute_name)

    def get_all_global_attributes(self) -> dict:
        """Returns all global attributes in the netCDF file.

        Returns:
        - dict: A dictionary of all global attributes in the netCDF file.
        """

        return self.nc.__dict__

    def get_all_variable_attributes(self, variable_name: str) -> dict:
        """Returns all attributes for a variable in the netCDF file.

        Parameters:
        - variable_name (str): The name of the variable to get attributes for.

        Returns:
        - dict: A dictionary of all attributes for the variable.
        """

        return self.nc.variables[variable_name].__dict__

    def add_multiple_global_attributes(self, attributes: dict):
        """Adds multiple global attributes to the netCDF file.

        If the attribute already exists, it will be overwritten.

        Parameters:
        - attributes (dict): A dictionary of attribute names and values to be added.
        """

        self.nc.setncatts(attributes)

    def add_multiple_variable_attributes(self, variable_name: str, attributes: dict):
        """Adds multiple attributes to a variable in the netCDF file.

        If the attribute already exists, it will be overwritten.

        Parameters:
        - variable_name (str): The name of the variable to which the attributes will be added.
        - attributes (dict): A dictionary of attribute names and values to be added.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        self.nc.variables[variable_name].setncatts(attributes)

    #####################################
    # Methods for writing data
    #####################################

    def write_time_data(self, timestamps: list[datetime]):
        """Writes timestamps to the 'time' variable in the netCDF file.

        Will overwrite any existing data in the 'time' variable.

        Parameters:
        - timestamps (list[datetime]): A list of datetime objects in UTC (no timezone offset)

        The list must be complete and in the correct order.


        Raises:
        - ValueError: If the timestamp has unsupported timezone information.
        - ValueError: If 'time' variable does not exist in the file.
        """

        if "time" not in self.nc.variables:
            raise ValueError("Variable 'time' does not exist in the file.")

        if any(
            [ts.tzinfo != None and ts.utcoffset() != timedelta(0) for ts in timestamps]
        ):

            raise ValueError(
                "Timestamp has unsupported timezone information. Please use UTC."
            )

        units = self.get_variable_attribute("time", "units")
        calender = self.get_variable_attribute("time", "calendar")

        nums = date2num(timestamps, units, calender)

        self.nc.variables["time"][:] = nums

    def write_scalar_data(self, variable_name: str, data: str | int | float):
        """Writes data to a scalar variable in the netCDF file.

        Will overwrite any existing data in the variable.

        Parameters:
        - variable_name (str): The name of the variable to write data to.
        - data (str|int|float): The data to be written.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        self.nc.variables[variable_name][:] = data

    def write_data(self, variable_name: str, data: any):
        """Writes data to a variable in the netCDF file.

        Will overwrite any existing data in the variable.

        Data must be in the correct shape and size to match the variable.

        None values will be converted to the missing value for the variable.

        Parameters:
        - variable_name (str): The name of the variable to write data to.
        - data (any): The data to be written.

        Raises:
        - ValueError: If the variable does not exist in the file.
        - ValueError: If the data shape does not match the variable shape.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        if not self.is_coordinate_variable(variable_name):
            missing_value = self.get_variable_attribute(variable_name, "missing_value")
            cleaned_data = convert_none_to_missing_value(data, missing_value)
        else:
            cleaned_data = data

        data_matrix = np.array(cleaned_data)

        variable_shape = self.nc.variables[variable_name].shape
        data_shape = data_matrix.shape

        if variable_shape != data_shape:
            raise ValueError(
                f"Data shape {data_shape} does not match variable shape {variable_shape}."
            )

        self.nc.variables[variable_name][:] = data_matrix

    #####################################
    # Methods for appending data
    #####################################

    def append_time_data(self, timestamps: list[datetime]):
        """Appends timestamps to the 'time' variable in the netCDF file.

        Parameters:
        - timestamps (list[datetime]): A list of datetime objects in UTC (no timezone offset)

        The list must be complete and in the correct order.


        Raises:
        - ValueError: If the timestamp has unsupported timezone information.
        - ValueError: If 'time' variable does not exist in the file.

        """
        if "time" not in self.nc.variables:
            raise ValueError("Variable 'time' does not exist in the file.")

        if any(
            [ts.tzinfo != None and ts.utcoffset() != timedelta(0) for ts in timestamps]
        ):

            raise ValueError(
                "Timestamp has unsupported timezone information. Please use UTC."
            )

        units = self.get_variable_attribute("time", "units")
        calender = self.get_variable_attribute("time", "calendar")

        nums = date2num(timestamps, units, calender)

        first_index = self.nc.variables["time"].shape[0]

        self.nc.variables["time"][first_index:] = nums

    def append_data(
        self, variable_name: str, data: any, ref_time: datetime, select: str
    ):
        """Appends data to a variable in the netCDF file.

        The variable must have 'time' as its first dimension.
        It is only possible to extend data along the time dimension.

        Data must be in the correct shape and size to match the variable.

        None values will be converted to the missing value for the variable.

        Parameters:
        - variable_name (str): The name of the variable to append data to.
        - data (any): The data to be appended.
        - ref_time (datetime): The reference time to use for the append operation.
            Based on the 'ref_time' the the index to insert data from will be found.
        - select (str): The selection method to use when finding the index to insert data from.
            - 'exact': Insert data at the exact reference time.
            - 'before': Insert data before the reference time.
            - 'after': Insert data after the reference time.
            - 'nearest': Insert data at the nearest time to the reference time.

        Raises:
        - ValueError: If the variable does not exist in the file.
        - ValueError: If the data shape does not match the variable shape.
        """
        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        if self.get_variable_dimensions(variable_name)[0] != "time":
            raise ValueError(
                f"Variable '{variable_name}' must have 'time' as its first dimension to append data. Selected variable have following dimensions: {self.get_variable_dimensions(variable_name)}"
            )

        if not self.is_coordinate_variable(variable_name):
            missing_value = self.get_variable_attribute(variable_name, "missing_value")
            cleaned_data = convert_none_to_missing_value(data, missing_value)
        else:
            cleaned_data = data

        data_matrix = np.array(cleaned_data)

        calendar = self.get_variable_attribute("time", "calendar")
        first_index = date2index(
            ref_time, self.nc.variables["time"], select=select, calendar=calendar
        )

        if data_matrix.shape[0] + first_index != self.nc.variables["time"].shape[0]:
            raise ValueError(
                f"Append of data to variable '{variable_name}' will result in a mismatch of the time dimension. Data length: {data_matrix.shape[0]+first_index}, Time dimension shape: {self.nc.variables['time'].shape[0]}"
            )

        self.nc.variables[variable_name][first_index:] = data_matrix

    #####################################
    # Methods for reading data - TBD
    #####################################

    def read_time_data(self) -> list[datetime]:
        """Reads the 'time' variable from the netCDF file.

        All masks will be applied to the data and only data that is not masked will be returned.

        Returns:
        - list[datetime]: A list of datetime objects in UTC (no timezone offset).

        Raises:
        - ValueError: If no masks have been set - run set_default_masks() first.

        """
        if self.masks is None:
            raise ValueError(
                "No masks have been set. Please set masks before reading data."
            )

        combined_mask = get_combined_mask(
            self.get_variable_dimensions("time"), self.masks
        )

        time_nums = self.nc.variables["time"][combined_mask]

        units = self.get_variable_attribute("time", "units")
        calender = self.get_variable_attribute("time", "calendar")

        real_datetimes = num2date(
            time_nums,
            units,
            calender,
            only_use_cftime_datetimes=False,
            only_use_python_datetimes=True,
        )

        return real_datetimes_to_datetimes(real_datetimes)

    def read_scalar_data(self, variable_name: str) -> str | int | float:
        """Reads a scalar variable from the netCDF file.

        Parameters:
        - variable_name (str): The name of the variable to read data from.

        Returns:
        - str|int|float: The data from the variable.

        Raises:
        - ValueError: If the variable does not exist in the file.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        return self.nc.variables[variable_name].getValue().item()

    def read_data(self, variable_name: str) -> list[any]:
        """Reads a variable from the netCDF file.

        All masks will be applied to the data and only data that is not masked will be returned.

        Items with values equal to the missing value will be converted to None.

        Items with values outside the valid range will be converted to None.

        Parameters:
        - variable_name (str): The name of the variable to read data from.

        Returns:
        - list[any]: The data from the variable, single list or a matrix of lists.

        Raises:
        - ValueError: If the variable does not exist in the file.
        - ValueError: If no masks have been set - run set_default_masks() first.
        """

        if variable_name not in self.nc.variables:
            raise ValueError(f"Variable '{variable_name}' does not exist in the file.")

        if self.masks is None:
            raise ValueError(
                "No masks have been set. Please set masks before reading data."
            )

        combined_mask = get_combined_mask(
            self.get_variable_dimensions(variable_name), self.masks
        )

        return self.nc.variables[variable_name][combined_mask].tolist()

    # TODO define methods for setting mask to be used when reading the data

    def set_default_masks(self):
        """Sets defaults masks for all dimensions

        Will overwrite any existing masks

        Default masks allows all data to be returned.

        Must be executed before reading data!
        """
        all_dims = self.get_all_dimensions()
        masks = {}

        for dim in all_dims:
            masks[dim] = slice(None)

        self.masks = masks

    def set_time_mask_from(self, time: datetime):
        """Sets a mask to filter data from a given time.

        If default masks have not been set, they will be set.

        Parameters:
        - time (datetime): The time to filter data from given in UTC.
        """
        if self.masks is None:
            self.set_default_masks()

        time_num = self.datetime_to_num(time)
        variable = self.nc.variables["time"]
        mask = np.ma.masked_greater_equal(variable[:], time_num).mask

        self.masks["time"] = fit_mask_to_shape(mask, variable.shape)

    def set_time_mask_to(self, time: datetime):
        """Sets a mask to filter data to a given time (including specified time).

        If default masks have not been set, they will be set.

        Parameters:
        - time (datetime): The time to filter data to given in UTC.
        """
        if self.masks is None:
            self.set_default_masks()

        time_num = self.datetime_to_num(time)
        variable = self.nc.variables["time"]
        mask = np.ma.masked_less_equal(variable[:], time_num).mask

        self.masks["time"] = fit_mask_to_shape(mask, variable.shape)

    def set_time_mask_between(self, start_time: datetime, end_time: datetime):
        """Sets a mask to filter data between two times.

        If default masks have not been set, they will be set.

        Parameters:
        - start_time (datetime): The start time to filter data from given in UTC.
        - end_time (datetime): The end time to filter data to given in UTC.
        """
        if self.masks is None:
            self.set_default_masks()

        start_time_num = self.datetime_to_num(start_time)
        end_time_num = self.datetime_to_num(end_time)
        variable = self.nc.variables["time"]
        mask = np.ma.masked_inside(variable[:], start_time_num, end_time_num).mask

        self.masks["time"] = fit_mask_to_shape(mask, variable.shape)

    def set_dimension_mask_from(self, dim: str, value: any):
        """Sets a mask to filter data from a given value for a dimension.

        If default masks have not been set, they will be set.

        Parameters:
        - dim (str): The dimension to filter data from.
        - value (any): The value to filter data from.

        Raises:
        - ValueError: If the mask has more than one dimension.
        """
        if self.masks is None:
            self.set_default_masks()

        variable = self.nc.variables[dim]
        mask = np.ma.masked_greater_equal(variable[:], value).mask

        if len(mask.shape) > 1:
            raise ValueError(
                f"Mask has more than one dimension, shape of mask: {mask.shape}"
            )

        self.masks[dim] = fit_mask_to_shape(mask, variable.shape)

    def set_dimension_mask_to(self, dim: str, value: any):
        """Sets a mask to filter data to a given value for a dimension (including specified value).

        If default masks have not been set, they will be set.

        Parameters:
        - dim (str): The dimension to filter data to.
        - value (any): The value to filter data to.

        Raises:
        - ValueError: If the mask has more than one dimension.
        """

        if self.masks is None:
            self.set_default_masks()

        variable = self.nc.variables[dim]
        mask = np.ma.masked_less_equal(variable[:], value).mask

        if len(mask.shape) > 1:
            raise ValueError(
                f"Mask has more than one dimension, shape of mask: {mask.shape}"
            )

        self.masks[dim] = fit_mask_to_shape(mask, variable.shape)

    def set_dimension_mask_between(self, dim: str, start_value: any, end_value: any):
        """Sets a mask to filter data between two values for a dimension.

        If default masks have not been set, they will be set.

        Parameters:
        - dim (str): The dimension to filter data from.
        - start_value (any): The start value to filter data from.
        - end_value (any): The end value to filter data to.

        Raises:
        - ValueError: If the mask has more than one dimension.
        """

        if self.masks is None:
            self.set_default_masks()

        variable = self.nc.variables[dim]
        mask = np.ma.masked_inside(variable[:], start_value, end_value).mask

        if len(mask.shape) > 1:
            raise ValueError(
                f"Mask has more than one dimension, shape of mask: {mask.shape}"
            )

        self.masks[dim] = fit_mask_to_shape(mask, variable.shape)

    def set_dimension_mask_exact(self, dim: str, value: any):
        """Sets a mask to filter data to a specific value for a dimension.

        If default masks have not been set, they will be set.

        Parameters:
        - dim (str): The dimension to filter data from.
        - value (any): The value to filter data for.

        Raises:
        - ValueError: If the mask has more than one dimension.
        """

        if self.masks is None:
            self.set_default_masks()

        variable = self.nc.variables[dim]
        mask = np.ma.masked_equal(variable[:], value).mask

        if len(mask.shape) > 1:
            raise ValueError(
                f"Mask has more than one dimension, shape of mask: {mask.shape}"
            )

        self.masks[dim] = fit_mask_to_shape(mask, variable.shape)

    def datetime_to_num(self, time: datetime) -> float:
        calendar = self.get_variable_attribute("time", "calendar")
        units = self.get_variable_attribute("time", "units")

        return date2num(time, units, calendar)
