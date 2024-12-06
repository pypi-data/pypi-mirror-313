from yta_general_utils.image.region import Region, Coordinate
from typing import Tuple, Union


class GreenscreenAreaDetails:
    """
    This class represents a greenscreen area inside of a greenscren
    video or image resource and will containg the used rgb color, 
    the position and more information.

    @param
    **rgb_color**
        The green color in rgb format: (r, g, b).
    @param
    **similar_greens**
        Similar green colors found in the image as a list in which
        each element is in rgb format: (r, g, b).
    @param
    **upper_left_pixel**
        The upper left pixel position in the format (x, y).
    @param
    **lower_right_pixel**
        The lower right pixel position in the format (x, y).
    @param
    **frames**
        The frames in which the greenscreen area is present in the
        (start, end) format. If the greenscreen area is present the
        whole video or the greenscreen is an image, this value
        will be None.
    
    """
    rgb_color = None
    similar_greens = None
    region: Region = None
    upper_left_pixel: Coordinate = None
    lower_right_pixel: Coordinate = None
    frames = None

    def __init__(self, rgb_color: Tuple[int, int, int] = (0, 0, 255), similar_greens = [], upper_left_pixel: Coordinate = Coordinate(0, 0), lower_right_pixel: Coordinate = Coordinate(0, 0), frames: Union[Tuple[int, int], None] = None):
        # TODO: Implement checkings please
        self.rgb_color = rgb_color
        self.similar_greens = similar_greens
        self.upper_left_pixel = upper_left_pixel
        self.lower_right_pixel = lower_right_pixel
        # TODO: This is to replace the 'upper_left_pixel' and 'lower_right_pixel'
        self.region = Region(self.upper_left_pixel.x, self.upper_left_pixel.y, self.lower_right_pixel.x, self.lower_right_pixel.y)
        self.frames = frames