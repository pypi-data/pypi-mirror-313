"""
This is an adaption of the rate functions found in manim
library for the moviepy library. I have to use lambda t
functions with the current frame time to be able to resize
or reposition a video, so I have adapted the manim rate
functions to be able to return a factor that, with specific
moviepy functions, will make a change with the factor that
has been calculated with the corresponding rate function.

You can see 'manim/utils/rate_functions.py'.

This is the way I have found to make it work and to be able
to build smoother animations. As manim docummentation says,
the rate functions have been inspired by the ones listed in
this web page: https://easings.net/
"""
from yta_general_utils.math.rate_functions import RateFunction
from yta_multimedia.video.edition.effect.moviepy.position.utils.shake import shake_movement, shake_decreasing_movement, shake_increasing_movement
from yta_multimedia.video.edition.effect.moviepy.position.utils import circles

import numpy as np


# TODO: This method is duplicated in
# yta_multimedia\video\edition\effect\moviepy\position\utils\__init__.py
def rate_function(t: float, duration: float, rate_func: type, *args, **kwargs):
    """
    You need to provide one of the functions of RateFunction class
    as the 'rate_func' parameter to be able to make it work, and 
    pass the needed args to it.
    """
    return rate_func(t / duration, *args, **kwargs)

class TFunctionResize:
    """
    Class to simplify and encapsulate the functionality
    related with the zoom of a video (by resizing it).

    You can use these methods to make a moviepy video
    rotate from the 'initial_size' to the 'final_size'
    using the 'rate_func'. The original video size is 1.
    """
    @staticmethod
    def resize_from_to(t: float, duration: float, initial_size: float, final_size: float, rate_func: type = RateFunction.linear, *args, **kwargs):
        """
        A function to be applied in moviepy '.resized()' as 'lambda t:
        zoom_from_to()'.

        A size value of 1 means no resize, while a value greater than 1
        is a zoom_in effect (enlarging it), and a value lower than 1 is
        a zoom_out effect (shortening it). The size must be always
        greater than 0.

        The 'rate_func' must be one of the existing functions in the
        yta_general_utils.math.rate_functions.RateFunction class.
        """
        # TODO: Check 'initial_size', 'final_size' and 'rate_func'
        # are valid
        # TODO: If size becomes smaller than 0 it is not valid because
        # PIL cannot handle 0 size.
        return initial_size + (final_size - initial_size) * rate_function(t, duration, rate_func, *args, **kwargs)

class TFunctionRotate:
    """
    Class to simplify and encapsulate the functionality
    related with the rotation of a video.

    You can use these methods to make a moviepy video
    rotate from the 'initial_rotation' to the 
    'final_rotation' using the 'rate_func'.
    """
    @staticmethod
    def rotate_from_to(t: float, duration: float, initial_rotation: int, final_rotation: int, rate_func: type = RateFunction.linear, *args, **kwargs):
        """
        A function to be applied in moviepy '.rotated()' as 'lambda
        t: rotate_from_to()'.

        The 'initial_rotation' and the 'final_rotation' must be, each
        one, the expected rotation, expressed in degrees.

        The 'rate_func' must be one of the existing functions in the
        yta_general_utils.math.rate_functions.RateFunction class.
        """
        # TODO: Check 'initial_rotation', 'final_rotation' and 
        # 'rate_func' are valid
        return initial_rotation + (final_rotation - initial_rotation) * rate_function(t, duration, rate_func, *args, *kwargs)

# TODO: I don't know where I should place this, but
# I keep it here by now as it is related with the
# t functions
# TODO: This below is related to positioning. As we
# know, we can set a rate_func for the movement, but
# the path has been always a straight line. Now this
# changes with the functions below:
class TFunctionSetPosition:
    """
    Class to simplify and encapsulate the functionality
    related with the path to follow between the point
    from which we want to go and where we want to reach.

    You can use these methods to make a moviepy video go
    from the 'initial_position' to the 'final_position'
    using the 'rate_func' but also choosing the path that
    the method is defining.
    """

    def linear(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        factor = rate_function(t, duration, rate_func)

        x = initial_position[0] + (final_position[0] - initial_position[0]) * factor
        y = initial_position[1] + (final_position[1] - initial_position[1]) * factor

        return (x, y)

    def linear_doing_circles(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.linear(t, duration, initial_position, final_position, rate_func)

        # TODO: What about using a linear function (?)
        return circles(t, duration, pos)
    
    def linear_with_normal_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.linear(t, duration, initial_position, final_position, rate_func)

        return shake_movement(t, pos[0], pos[1])
    
    def linear_with_decreasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.linear(t, duration, initial_position, final_position, rate_func)

        return shake_decreasing_movement(t, pos[0], pos[1], duration)
    
    def linear_with_increasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.linear(t, duration, initial_position, final_position, rate_func)

        return shake_increasing_movement(t, pos[0], pos[1], duration)
    
    def sinusoidal(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        """
        Returns the (x, y) position tuple for the moviepy '.with_position()' method,
        for each 't' provided, that will make the element move doing a sinusoidal
        movement from the 'initial_position' to the 'final_position' in the provided
        'duration' time.
        """
        sinusoidal_wave_amplitude = 100
        sinusoidal_wave_frequency = 2
        factor = rate_function(t, duration, rate_func)

        x = initial_position[0] + factor * (final_position[0] - initial_position[0])
        y = initial_position[1] + factor * (final_position[1] - initial_position[1]) + sinusoidal_wave_amplitude * np.sin(2 * np.pi * sinusoidal_wave_frequency * factor)

        return (x, y)
    
    def sinusoidal_doing_circles(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.sinusoidal(t, duration, initial_position, final_position, rate_func)

        # TODO: What about using a linear function (?)
        return circles(t, duration, pos)
    
    def sinusoidal_with_normal_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.sinusoidal(t, duration, initial_position, final_position, rate_func)

        return shake_movement(t, pos[0], pos[1])
    
    def sinusoidal_with_decreasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.sinusoidal(t, duration, initial_position, final_position, rate_func)

        return shake_decreasing_movement(t, pos[0], pos[1], duration)

    def sinusoidal_with_increasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.sinusoidal(t, duration, initial_position, final_position, rate_func)

        return shake_increasing_movement(t, pos[0], pos[1], duration)
    
    def zigzag(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        factor = rate_function(t, duration, rate_func)
        amplitude = 15
        
        x = initial_position[0] + factor * (final_position[0] - initial_position[0])
        y = initial_position[1] + factor * (final_position[1] - initial_position[1]) + amplitude * np.sin(10 * np.pi * factor)

        return (x, y)

    def zigzag_doing_circles(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.zigzag(t, duration, initial_position, final_position, rate_func)

        # TODO: What about using a linear function (?)
        return circles(t, duration, pos)
    
    def zigzag_with_normal_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.zigzag(t, duration, initial_position, final_position, rate_func)

        return shake_movement(t, pos[0], pos[1])
    
    def zigzag_with_decreasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.zigzag(t, duration, initial_position, final_position, rate_func)

        return shake_decreasing_movement(t, pos[0], pos[1], duration)
    
    def zigzag_with_increasing_shaking(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        pos = TFunctionSetPosition.zigzag(t, duration, initial_position, final_position, rate_func)

        return shake_increasing_movement(t, pos[0], pos[1], duration)
    
    # TODO: Below code is not working properly

    # TODO: This is not working properly, from upper left to
    # bottom right it makes just a horizontal movement
    def wave(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        """
        Returns the (x, y) position tuple for the moviepy '.with_position()'
        method, for each 't' provided, that will make the element go to the
        'initial_position' to the 'final_position' by doing two arcs (a 
        wave), one top and one bottom.
        """
        # TODO: Fix the 'y', it is not starting from the initial 
        # point
        sinusoidal_wave_amplitude = 200  # Maximum height of the arc
        sinusoidal_wave_frequency = 2 * np.pi / (final_position[0] - initial_position[0])  # Controls the frequency of the sine wave
        offset = (final_position[0] - initial_position[0]) / 2  # Center of the arc
        factor = rate_function(t, duration, rate_func)
        x = initial_position[0] + (final_position[0] - initial_position[0]) * factor

        # Sinusoidal curve: y = amplitude * sin(frequency * (x - offset)) + average_y
        average_y = (initial_position[1] + final_position[1]) / 2
        y = sinusoidal_wave_amplitude * np.sin(sinusoidal_wave_frequency * (x - initial_position[0] - offset)) + average_y
        
        return (x, y)
    
    # TODO: This is not working properly, from upper left to
    # bottom right it makes just a horizontal movement
    # TODO: I need to avoid additional parameters, I must keep
    # only 't', 'initial_position', 'final_position' and 
    # 'rate_func' because it is the basic structure, so I can
    # create '.arc_bottom' and '.arc_top' if needed.
    def arc(t: float, duration: float, initial_position: tuple, final_position: tuple, arc_is_bottom: bool = False, rate_func: type = RateFunction.linear):
        """
        Returns the (x, y) position tuple for the moviepy '.with_position()'
        method, for each 't' provided, that will make the element go to the
        'initial_position' to the 'final_position' by doing one single 
        arc movement. The movement will be an arc above, or bottom if the
        'arc_is_bottom' parameter is set as True. The 'max_height' parameter
        is to set the maximum height of the arc.
        """
        # TODO: Fix the 'y', it is not starting from the initial 
        # point
        max_height = 300
        factor = rate_function(t, duration, rate_func)
        x = initial_position[0] + (final_position[0] - initial_position[0]) * factor

        # Calculate the midpoint and the maximum y value
        midpoint_x = (initial_position[0] + final_position[0]) / 2
        midpoint_y = (initial_position[1] + final_position[1]) / 2
        if arc_is_bottom:
            midpoint_y += max_height
        else:
            midpoint_y -= max_height

        # Calculate the arc movement:   y = a(x - h)^2 + k
        if arc_is_bottom:
            a = 4 * max_height / ((final_position[0] - initial_position[0])**2)
            y = -a * (x - midpoint_x)**2 + midpoint_y
        else:
            a = -4 * max_height / ((final_position[0] - initial_position[0])**2)
            y = -a * (x - midpoint_x)**2 + midpoint_y
        
        return (x, y)
    
    # TODO: This is not working properly
    def circles(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear):
        # TODO: Fix the 'y', it is not starting from the initial 
        # point
        from math import sqrt, atan2, cos, sin

        factor = rate_function(t, duration, rate_func)
        # Desempaquetar las coordenadas iniciales y finales
        x1, y1 = initial_position
        x2, y2 = final_position

        # Calcular el vector de dirección
        dx = x2 - x1
        dy = y2 - y1
        distancia = sqrt(dx**2 + dy**2)

        # Calcular el centro del círculo
        # El centro está a medio camino de A y B, pero desplazado perpendicularmente
        # La dirección perpendicular al vector AB
        perpendicular_dx = -dy
        perpendicular_dy = dx
        
        # Normalizar el vector perpendicular
        longitud_perpendicular = sqrt(perpendicular_dx**2 + perpendicular_dy**2)
        perpendicular_dx /= longitud_perpendicular
        perpendicular_dy /= longitud_perpendicular
        
        # El radio del círculo es la mitad de la distancia entre A y B
        radio = distancia / 2
        
        # El centro del círculo está a la mitad de la distancia entre A y B y desplazado en la dirección perpendicular
        cx = (x1 + x2) / 2 + radio * perpendicular_dx
        cy = (y1 + y2) / 2 + radio * perpendicular_dy

        # El ángulo de inicio del movimiento (desde A)
        angulo_inicio = atan2(y1 - cy, x1 - cx)
        
        # El ángulo final del movimiento (hacia B)
        angulo_final = atan2(y2 - cy, x2 - cx)
        
        # Hacer que el objeto se mueva de A a B a través del círculo en función de t (que va de 0 a 1)
        # Convertir t en un ángulo dentro del círculo
        angulo_actual = angulo_inicio + (angulo_final - angulo_inicio) * factor
        
        # Coordenadas del objeto en la trayectoria circular
        x = cx + radio * cos(angulo_actual)
        y = cy + radio * sin(angulo_actual)
        
        return (x, y)