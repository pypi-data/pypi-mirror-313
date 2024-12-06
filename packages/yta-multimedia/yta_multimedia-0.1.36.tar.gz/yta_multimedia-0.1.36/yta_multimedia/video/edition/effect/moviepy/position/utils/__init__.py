from yta_general_utils.math.rate_functions import RateFunction
from math import pi

import numpy as np


# TODO: This method is duplicated in
# yta_multimedia\video\edition\effect\moviepy\t_function\__init__.py
def rate_function(t: float, duration: float, rate_func: type, *args, **kwargs):
    """
    You need to provide one of the functions of RateFunction class
    as the 'rate_func' parameter to be able to make it work, and 
    pass the needed args to it.
    """
    return rate_func(t / duration, *args, **kwargs)

def circles(t: float, duration: float, position: tuple, radius: int = 200, time_per_circle: float = 1, rate_func: type = RateFunction.linear):
        """
        Returns the (x, y) position tuple for the moviepy '.with_position()' effect,
        for each 't' provided, that will make the element move in circles with the
        provided 'radius'. The 'radius' parameter is the distance between the origin
        and the path the clip will follow. The 'cicle_time' is the time (in seconds)
        needed for a complete circle to be completed by the movement.

        If you provide the video duration as 'cicle_time', the video will make only
        one whole circle
        """
        circle_factor = rate_function(t % time_per_circle, time_per_circle, rate_func)

        # TODO: Do checkings
        return position[0] + radius * np.cos((circle_factor) * 2 * pi), position[1] + radius * np.sin((circle_factor) * 2 * pi)
        # Working code was this below:
        # return x + radius * np.cos((t / time_per_circle) * 2 * math.pi), y + radius * np.sin((t / time_per_circle) * 2 * math.pi)