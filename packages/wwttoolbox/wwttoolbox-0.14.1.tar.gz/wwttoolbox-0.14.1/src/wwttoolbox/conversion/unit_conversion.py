import math


def convert_W_2_MJ(data: float | int | list[float | int]) -> float | list[float]:
    """
    Convert Watt to MegaJoule

    Parameters
    ----------
    data : float or list of float
        Watt value(s) to be converted

    Returns
    -------
    float or list of float
        MegaJoule value(s)
    """
    transformed_data = data if isinstance(data, list) else [data]

    converted_data = []

    for value in transformed_data:
        converted_data.append(value * 3600 / 1e6)

    return converted_data if isinstance(data, list) else converted_data[0]


def convert_percentage_2_fraction(
    data: float | int | list[float | int],
) -> float | list[float]:
    """
    Convert percentage to fraction

    Parameters
    ----------
    data : float or list of float|int
        Percentage value(s) to be converted

    Returns
    -------
    float or list of float
        Fraction value(s)
    """
    transformed_data = data if isinstance(data, list) else [data]

    converted_data = []

    for value in transformed_data:
        converted_data.append(value / 100)

    return converted_data if isinstance(data, list) else converted_data[0]


def convert_wind_speed_and_direction_2_u_v_components(
    wind_speed: float | int | list, wind_direction: float | int | list
) -> dict[str, float | list[float]]:
    """
    Convert wind speed and direction to u and v components

    Parameters
    ----------
    wind_speed : float, int or list of float|int
        Wind speed in m/s
    wind_direction : float, int or list of float|int
        Wind direction in degrees

    Returns
    -------
    dict
        u and v components of wind speed
    """
    if isinstance(wind_speed, list) != isinstance(wind_direction, list):
        raise ValueError("Wind speed and wind direction must be of the same type")

    transformed_wind_speed = (
        wind_speed if isinstance(wind_speed, list) else [wind_speed]
    )
    transformed_wind_direction = (
        wind_direction if isinstance(wind_direction, list) else [wind_direction]
    )

    theta = [(270 - value) / 180 * math.pi for value in transformed_wind_direction]

    u = [value * math.cos(angle) for value, angle in zip(transformed_wind_speed, theta)]
    v = [value * math.sin(angle) for value, angle in zip(transformed_wind_speed, theta)]

    if isinstance(wind_speed, list):
        return {"u": u, "v": v}
    else:
        return {"u": u[0], "v": v[0]}
