import netCDF4 as nc4
from datetime import datetime, timezone
from cftime import real_datetime
import numpy as np


def convert_simple_dtype_to_nc_dtype(data_type: str) -> str:
    """Converts a data type to the netCDF compatible data type.

    Parameters:
    - data_type (str): The data type to be converted.

    dType options:
    - int: 16-bit integer (i2)
    - long: 32-bit integer (i4)
    - float: 32-bit floating point (f4)
    - double: 64-bit floating point (f8)
    - all netCDF supported data types

    Returns:
    - str: The netCDF compatible data type.
    """

    data_type = data_type.lower()

    if data_type == "int":
        return "i2"
    elif data_type == "long":
        return "i4"
    elif data_type == "float":
        return "f4"
    elif data_type == "double":
        return "f8"
    elif data_type in nc4.default_fillvals.keys():
        return data_type
    else:
        raise ValueError(f"Invalid data type: {data_type}")


def convert_nc_dtype_to_simple_dtype(data_type: str) -> str:
    """Converts a netCDF compatible data type to a simple data type.

    Parameters:
    - data_type (str): The netCDF compatible data type to be converted.

    Returns:
    - str: The simple data type.
    """

    if data_type == "i2":
        return "int"
    elif data_type == "i4":
        return "long"
    elif data_type == "f4":
        return "float"
    elif data_type == "f8":
        return "double"
    else:
        return data_type


def get_related_missing_value_to_simple_dtype(dtype: str) -> str:
    """Returns the missing value for the given data type.

    Parameters:
    - dtype (str): The data type to get the missing value for.

    Returns:
    - number: Default value based on the netCDF4.default_fillvals
    """

    dtype = convert_simple_dtype_to_nc_dtype(dtype)
    return nc4.default_fillvals[dtype]


def convert_none_to_missing_value(data: any, missing_value: any):
    """Converts None values in data to missing value.

    Parameters:
    - data (any): The data to be converted.
    - missing_value (any): The missing value to be used.

    Returns:
    - any: The data with None values converted to missing value.
    """

    masked_data = np.ma.masked_where(np.array(data) == None, data)

    return masked_data.filled(missing_value).tolist()


def real_datetimes_to_datetimes(real_datetimes: list[real_datetime]) -> list[datetime]:
    """Converts a list of cftime.real_datetime objects to datetime objects.

    Parameters:
    - real_datetimes (list): The list of cftime.real_datetime objects to be converted.

    Returns:
    - list: The list of datetime objects in UTC.
    """

    return [
        datetime.fromisoformat(real_datetime.isoformat()).replace(tzinfo=timezone.utc)
        for real_datetime in real_datetimes
    ]
