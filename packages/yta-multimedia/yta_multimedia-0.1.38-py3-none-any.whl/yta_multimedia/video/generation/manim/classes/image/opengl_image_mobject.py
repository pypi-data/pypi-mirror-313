from yta_general_utils.programming.parameter_validator import PythonValidator
from manim.mobject.opengl.opengl_image_mobject import OpenGLImageMobject as OriginalOpenGLImageMobject
from pathlib import Path
from PIL import Image
from typing import Union

import numpy as np


class OpenGLImageMobject:
    """
    Custom class created to use its 'init' method to solve a problem with
    filename passed as a parameter, that is not correctly parsed by the
    original manim OpenGLImageMobject class.

    This class is not instantiable, just use OpenGLImageMobject.init(params)
    to obtain a real manim OpenGLImageMobject instance.
    """
    # TODO: I would like to use it as OpenGLImageMobject and that init method
    # return an instance of the original manim OpenGLImageMobject and not this
    # one, but as I don't know exactly how to do it I'm creating this static
    # 'init' method to achieve it. Improve it if possible, thanks.
    @staticmethod
    def init(
        filename_or_array: Union[str, Path, np.ndarray],
        width: float = None,
        height: float = None,
        image_mode: str = "RGBA",
        resampling_algorithm: int = Image.Resampling.BICUBIC,
        opacity: float = 1,
        gloss: float = 0,
        shadow: float = 0,
        **kwargs
    ):
        """
        This method returns an instance of a manim OpenGLImageMobject.
        """
        if PythonValidator.is_string(filename_or_array):
            filename_or_array = np.asarray(Image.open(filename_or_array))

        return OriginalOpenGLImageMobject(filename_or_array, width, height, image_mode, resampling_algorithm, opacity, gloss, shadow, **kwargs)

    def __init__(self):
        """
        DO NOT USE THIS METHOD. This class is not instantiable.
        """
        raise Exception('Sorry, this class is not instantiable, just use the "init" method to obtain a OpenGLImageMobject instance.')