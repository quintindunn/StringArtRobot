from numpy import sqrt, atan2, cos, sin
from math import pi


def cartesian_to_polar(x, y) -> tuple[float, float]:
    """
    Converts cartesian coordinates to polar coordinates.
    :param x: The x coordinate.
    :param y: The y coordinate.
    :return: Tuple[float, float] containing r, theta
    """
    r = sqrt(x ** 2 + y ** 2)
    theta = atan2(y, x)
    return r, theta


def polar_to_cartesian(r: int | float, theta: int | float) -> tuple[float, float]:
    """
    Converts polar coordinates to cartesian coordinates.
    :param r: The r value of the coordinates.
    :param theta: The theta value of the coordinates.
    :return: tuple[float, float] of the cartesian coordinates.
    """
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y


def rad_to_deg(rad: float):
    """
    Converts from radians to degrees
    :param rad: Radians
    :return: Degrees
    """
    return rad * 180/pi


def deg_to_rad(deg: float):
    """
    Converts from degrees to radians
    :param deg: Degrees
    :return: Radians
    """
    return deg * pi/180
