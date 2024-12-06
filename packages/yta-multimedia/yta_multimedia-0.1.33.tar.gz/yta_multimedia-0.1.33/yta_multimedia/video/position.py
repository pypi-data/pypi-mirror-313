from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_general_utils.random import randrangefloat
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.image.region import NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from random import choice as randchoice


class Position(Enum):
    """
    Enum class that represents a position within an specific
    scene. This is used to position a video or an image in that
    scene in an specific position defined by itself. It is
    useful with Manim and Moviepy video positioning and has
    been prepared to work with those engines.

    This position is always considered in a scene of 1920x1080.

    This position is a static position which means that it can
    be calculated by itself, without the need of any element
    size or similar. The coordinate that represent any of this
    """
    CENTER = 'center'
    """
    Just on the center of the scene
    """
    IN_EDGE_TOP = 'in_edge_top'
    """
    Just on the top edge of the scene.
    """
    IN_EDGE_BOTTOM = 'in_edge_bottom'
    IN_EDGE_RIGHT = 'in_edge_right'
    IN_EDGE_LEFT = 'in_edge_left'

    IN_EDGE_TOP_LEFT = 'in_edge_top_left'
    """
    Just on the upper left edge corner of the scene.
    """
    IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
    IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
    IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'

    HALF_LEFT = 'half_left'
    """
    Between the left edge and the center of the scene.
    """
    HALF_TOP_LEFT = 'half_top_left'
    HALF_TOP = 'half_top'
    HALF_TOP_RIGHT = 'half_top_right'
    HALF_RIGHT = 'half_right'
    HALF_BOTTOM_RIGHT = 'half_bottom_right'
    HALF_BOTTOM = 'half_bottom'
    HALF_BOTTOM_LEFT = 'half_bottom_left'

    OUT_LEFT = 'out_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the left of this one.
    """
    OUT_TOP = 'out_top'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top of this one.
    """
    OUT_RIGHT = 'out_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the right of this one.
    """
    OUT_BOTTOM = 'out_bottom'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom of this one.
    """
    OUT_TOP_LEFT = 'out_top_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top and left of this one.
    """
    OUT_TOP_RIGHT = 'out_top_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top and right of this one.
    """
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom and left of this one.
    """
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom and right of this one.
    """
    RANDOM_INSIDE = 'random_inside'
    RANDOM_OUTSIDE = 'random_outside'

    @staticmethod
    def get_outside_elements_list():
        """
        Return all the positions that are outside of 
        the screen as a list.
        """
        return [
            Position.OUT_BOTTOM,
            Position.OUT_BOTTOM_LEFT,
            Position.OUT_BOTTOM_RIGHT,
            Position.OUT_RIGHT,
            Position.OUT_LEFT,
            Position.OUT_TOP,
            Position.OUT_TOP_LEFT,
            Position.OUT_TOP_RIGHT
        ]
    
    @staticmethod
    def get_inside_elements_list():
        """
        Return all the positions that are inside of the 
        screen as a list.
        """
        return list(set(Position.get_all()) - set(Position.get_outside_elements_list()) - set([Position.RANDOM_INSIDE]) - set([Position.RANDOM_OUTSIDE]))

    @staticmethod
    def get_random_outside() -> 'Position':
        """
        Return a random position which is outside of the
        screen.
        """
        return randchoice(Position.get_outside_elements_list())
    
    @staticmethod
    def get_random_inside() -> 'Position':
        """
        Return a random position which is inside of the
        screen.
        """
        return randchoice(Position.get_inside_elements_list())

    def get_moviepy_center_tuple(self, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That
        position belongs to a coordinate in which you can place
        the center of any element.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            validate_size(scene_size, 'scene_size')

        # Alias to simplify :)
        w, h = scene_size

        if self == Position.RANDOM_INSIDE:
            return Position.get_random_inside().get_moviepy_center_tuple()
        elif self == Position.RANDOM_OUTSIDE:
            return Position.get_random_outside().get_moviepy_center_tuple()

        elif self == Position.CENTER:
            position = (w / 2, h / 2)

        elif self == Position.IN_EDGE_TOP:
            position = (w / 2, 0)
        elif self == Position.IN_EDGE_BOTTOM:
            position = (w / 2, h)
        elif self == Position.IN_EDGE_LEFT:
            position = (0, h / 2)
        elif self == Position.IN_EDGE_RIGHT:
            position = (w, h / 2)
        
        elif self == Position.IN_EDGE_TOP_LEFT:
            position = (0, 0)
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position = (w, 0)
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position = (w, h)
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position = (0, h)
        
        elif self == Position.HALF_LEFT:
            position = (w / 4, h / 2)
        elif self == Position.HALF_TOP_LEFT:
            position = (w / 4, h / 4)
        elif self == Position.HALF_TOP:
            position = (w / 2, h / 4)
        elif self == Position.HALF_TOP_RIGHT:
            position = (3 * w / 4, h / 4)
        elif self == Position.HALF_RIGHT:
            position = (3 * w / 4, h / 2)
        elif self == Position.HALF_BOTTOM_RIGHT:
            position = (3 * w / 4, 3 * h / 4)
        elif self == Position.HALF_BOTTOM:
            position = (w / 2, 3 * h / 4)
        elif self == Position.HALF_BOTTOM_LEFT:
            position = (w / 4, 3 * h / 4)

        elif self == Position.OUT_LEFT:
            position = (-w, h / 2)
        elif self == Position.OUT_TOP:
            position = (w / 2, -h / 2)
        elif self == Position.OUT_RIGHT:
            position = (w + w / 2, h / 2)
        elif self == Position.OUT_BOTTOM:
            position = (w / 2, h + h / 2)
        elif self == Position.OUT_TOP_LEFT:
            position = (-w, -h / 2)
        elif self == Position.OUT_TOP_RIGHT:
            position = (w + w / 2, -h / 2)
        elif self == Position.OUT_BOTTOM_LEFT:
            position = (-w, h + h / 2)
        elif self == Position.OUT_BOTTOM_RIGHT:
            position = (w + w / 2, h + h / 2)

        return position
    
    def get_moviepy_upper_left_corner_tuple(self, video_size: tuple, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video upper left corner to make its center be
        placed in this position.

        This method is useful to position a video in this desired
        position as it returns the value that can be directly used
        in 'with_position' method.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        if video_size is None:
            raise Exception('No "video_size" provided.')
        
        validate_size(video_size, 'video_size')
        
        # Obtain the position in which the center of the video
        # must be placed
        center_position = self.get_moviepy_center_tuple(scene_size)
        # TODO: Maybe force integer value (?)

        # Obtain the position in which we should place the video
        # (the upper left corner) to make the center of the video
        # be on that 'position_in_scene' position
        upper_left_corner = (center_position[0] - video_size[0] / 2, center_position[1] - video_size[1] / 2)

        return upper_left_corner
    
    def get_manim_position_center(self):
        """
        Get the position tuple (x, y, z) of this position according
        to the manim scene. That position belongs to a coordinate
        in which we need to put the manim video center to make its
        center be placed in this position.

        The 'z' value is always 0 as this is for a 2D scene.

        This works considering the upper left corner as the 
        (-HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT) coordinate.
        """
        # Alias to simplify :)
        hw, hh = HALF_SCENE_WIDTH, HALF_SCENE_WIDTH

        if self == Position.RANDOM_INSIDE:
            return Position.get_random_inside().get_manim_position_center()
        elif self == Position.RANDOM_OUTSIDE:
            return Position.get_random_outside().get_manim_position_center()

        elif self == Position.CENTER:
            position = 0, 0, 0

        elif self == Position.IN_EDGE_TOP:
            position = 0, hh, 0
        elif self == Position.IN_EDGE_BOTTOM:
            position = 0, -hh, 0
        elif self == Position.IN_EDGE_LEFT:
            position = -hw, 0, 0
        elif self == Position.IN_EDGE_RIGHT:
            position = hw, 0, 0

        elif self == Position.IN_EDGE_TOP_LEFT:
            position = -hw, hh, 0
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position = hw, hh, 0
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position = hw, -hh, 0
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position = -hw, -hh, 0
        
        elif self == Position.HALF_LEFT:
            position = -hw / 2, 0, 0
        elif self == Position.HALF_TOP_LEFT:
            position = -hw / 2, hh / 2, 0
        elif self == Position.HALF_TOP:
            position = 0, hh / 2, 0
        elif self == Position.HALF_TOP_RIGHT:
            position = hw / 2, hh / 2, 0
        elif self == Position.HALF_RIGHT:
            position = hw / 2, 0, 0
        elif self == Position.HALF_BOTTOM_RIGHT:
            position = hw / 2, -hh / 2, 0
        elif self == Position.HALF_BOTTOM:
            position = 0, -hh / 2, 0
        elif self == Position.HALF_BOTTOM_LEFT:
            position = -hw / 2, -hh / 2, 0

        elif self == Position.OUT_LEFT:
            position = 2 * -hw, 0, 0
        elif self == Position.OUT_TOP:
            position = 0, 2 * hh, 0
        elif self == Position.OUT_RIGHT:
            position = 2 * hw, 0, 0
        elif self == Position.OUT_BOTTOM:
            position = 0, 2 * -hh, 0
        elif self == Position.OUT_TOP_LEFT:
            position = 2 * -hw, 2 * hh
        elif self == Position.OUT_TOP_RIGHT:
            position = 2 * hw, 2 * hh
        elif self == Position.OUT_BOTTOM_LEFT:
            position = 2 * -hw, 2 * -hh
        elif self == Position.OUT_BOTTOM_RIGHT:
            position = 2 * hw, 2 * -hh

        return position

    @staticmethod
    def to_coordinate(position: 'Position'):
        """
        Turn the provided 'position' (that must be a tuple of
        2 elements) a coordinate.
        """
        position = Position.to_enum(position)

        position = position.get_moviepy_center_tuple()

        return Coordinate(position[0], position[1])
    
    # We don't need any upper left for manim because it
    # uses the center of the elements to position them
    
class DependantPosition(Enum):
    """
    Enum class that represents different positions within an
    scene of 1920x1080 that need a calculation because it
    depends on the size of the element we are trying to 
    position.
    """
    # TODO: Avoid the ones in Position that should not
    # be replaced
    TOP = 'top'
    TOP_RIGHT = 'top_right'
    RIGHT = 'right'
    BOTTOM_RIGHT = 'bottom_right'
    BOTTOM = 'bottom'
    BOTTOM_LEFT = 'bottom_left'
    LEFT = 'left'
    TOP_LEFT = 'top_left'

    OUT_TOP = 'out_top'
    OUT_TOP_RIGHT = 'out_top_right'
    OUT_RIGHT = 'out_right'
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    OUT_BOTTOM = 'out_bottom'
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    OUT_LEFT = 'out_left'
    OUT_TOP_LEFT = 'out_top_left'

    QUADRANT_1_TOP_RIGHT_CORNER = 'quadrant_1_top_right_corner'
    QUADRANT_1_BOTTOM_RIGHT_CORNER = 'quadrant_1_bottom_right_corner'
    QUADRANT_1_BOTTOM_LEFT_CORNER = 'quadrant_1_bottom_left_corner'
    QUADRANT_2_TOP_LEFT_CORNER = 'quadrant_2_top_left_corner'
    QUADRANT_2_BOTTOM_RIGHT_CORNER = 'quadrant_2_bottom_right_corner'
    QUADRANT_2_BOTTOM_LEFT_CORNER = 'quadrant_2_bottom_left_corner'
    QUADRANT_3_TOP_RIGHT_CORNER = 'quadrant_3_top_right_corner'
    QUADRANT_3_TOP_LEFT_CORNER = 'quadrant_3_top_left_corner'
    QUADRANT_3_BOTTOM_LEFT_CORNER = 'quadrant_3_bottom_left_corner'
    QUADRANT_4_TOP_RIGHT_CORNER = 'quadrant_4_top_right_corner'
    QUADRANT_4_TOP_LEFT_CORNER = 'quadrant_4_top_left_corner'
    QUADRANT_4_BOTTOM_RIGHT_CORNER = 'quadrant_4_bottom_right_corner'

    RANDOM_INSIDE = 'random_inside'
    RANDOM_OUTSIDE = 'random_outside'

    @staticmethod
    def _get_outside_items_as_list():
        """
        Get a list of the DependantPosition items that are placed
        outside of the screen limits.
        """
        return [
            DependantPosition.OUT_TOP_LEFT,
            DependantPosition.OUT_TOP,
            DependantPosition.OUT_RIGHT,
            DependantPosition.OUT_BOTTOM_RIGHT,
            DependantPosition.OUT_BOTTOM,
            DependantPosition.OUT_BOTTOM_LEFT,
            DependantPosition.OUT_LEFT
        ]
    
    @staticmethod
    def get_random_outside():
        """
        Get one random DependantPosition element that is placed
        outside of the screen limits.
        """
        return randchoice(DependantPosition._get_outside_items_as_list())

    @staticmethod
    def _get_inside_items_as_list():
        """
        Get a list of the DependantPosition items that are placed
        inside of the screen limits.
        """
        return list(set(DependantPosition.get_all()) - set(DependantPosition._get_outside_items_as_list()) - set([DependantPosition.RANDOM_INSIDE]) - set([DependantPosition.RANDOM_OUTSIDE]))

    @staticmethod
    def get_random_inside():
        """
        Get one random DependantPosition element that is placed
        inside of the screen limits.
        """
        return randchoice(DependantPosition._get_inside_items_as_list())

    def get_moviepy_position_center(self, video_size: tuple = (1920, 1080), scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video center to be placed in the desired
        position.

        This method is useful cannot be used directly to position
        a video as it is returning the coordinate in which the
        center must be placed and moviepy uses the upper left
        corner to be positioned, so consider using the method
        'get_moviepy_position_upper_left_corner' to obtain it.

        This works considering the upper left corner of the scene
        as the (0, 0) coordinate.
        """
        if video_size is None:
            video_size = (1920, 1080)
        else:
            validate_size(video_size, 'video_size')

        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            validate_size(scene_size, 'scene_size')
            
        # Alias to simplify :)
        sw, sh = scene_size
        vw, vh = video_size

        if self == DependantPosition.TOP:
            position = sw / 2, -vh / 2
        elif self == DependantPosition.RIGHT:
            position = sw - vw / 2, sh / 2
        elif self == DependantPosition.BOTTOM:
            position = sw / 2, sh - vh
        elif self == DependantPosition.LEFT:
            position = vw / 2, sh / 2

        elif self == DependantPosition.TOP_RIGHT:
            position = sw - vw / 2, vh / 2
        elif self == DependantPosition.BOTTOM_RIGHT:
            position = sw - vw / 2, sh - vh / 2
        elif self == DependantPosition.BOTTOM_LEFT:
            position = vw / 2, sh - vh / 2
        elif self == DependantPosition.TOP_LEFT:
            position = vw / 2, vh / 2

        elif self == DependantPosition.OUT_TOP:
            position = sw / 2, -vh / 2
        elif self == DependantPosition.OUT_TOP_RIGHT:
            position = sw + vw / 2, -vh / 2
        elif self == DependantPosition.OUT_RIGHT:
            position = sw + vw / 2, sh / 2
        elif self == DependantPosition.OUT_BOTTOM_RIGHT:
            position = sw + vw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_BOTTOM:
            position = sw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_BOTTOM_LEFT:
            position = -vw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_LEFT:
            position = -vw / 2, sh / 2
        elif self == DependantPosition.OUT_TOP_LEFT:
            position = -vw / 2, -vh / 2

        elif self == DependantPosition.QUADRANT_1_TOP_RIGHT_CORNER:
            position = sw / 2 - vw / 2, vh / 2
        elif self == DependantPosition.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position = vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_2_TOP_LEFT_CORNER:
            position = sw / 2 + vw / 2, vh / 2
        elif self == DependantPosition.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position = sw - vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_3_TOP_RIGHT_CORNER:
            position = sw - vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_3_TOP_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh - vh / 2
        elif self == DependantPosition.QUADRANT_4_TOP_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_4_TOP_LEFT_CORNER:
            position = vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh - vh / 2

        return position

    def get_moviepy_position_upper_left_corner(self, video_size: tuple, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video upper left corner to make its center be
        placed in this position.

        This method is useful to position a video in this desired
        position as it returns the value that can be directly used
        in 'with_position' method.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        # Obtain the position in which the center of the video
        # must be placed
        center_position = self.get_moviepy_position_center(video_size, scene_size)
        # TODO: Maybe force integer value (?)

        # Obtain the position in which we should place the video
        # (the upper left corner) to make the center of the video
        # be on that previously obtained 'center_position' position
        upper_left_corner = (center_position[0] - video_size[0] / 2, center_position[1] - video_size[1] / 2)

        return upper_left_corner

    def get_manim_position_center(self, video_size: tuple):
        if video_size is None:
            raise Exception('No "video_size" provided.')
        
        validate_size(video_size, 'video_size')
        
        # Alias to simplify :)
        hsw, hsh = HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT
        vw, vh = video_size

        # TODO: Process
        if self == DependantPosition.TOP:
            position = 0, hsh - vh / 2, 0
        elif self == DependantPosition.TOP_RIGHT:
            position = hsw - vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.RIGHT:
            position = hsw - vw / 2, 0, 0
        elif self == DependantPosition.BOTTOM_RIGHT:
            position = hsw - vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.BOTTOM:
            position = 0, -hsh + vh / 2, 0
        elif self == DependantPosition.BOTTOM_LEFT:
            position = -hsw + vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.LEFT:
            position = -hsw + vw / 2, 0, 0
        elif self == DependantPosition.TOP_LEFT:
            position = -hsw + vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.OUT_TOP_LEFT:
            position = -hsw - vw / 2, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_TOP:
            position = 0, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_TOP_RIGHT:
            position = hsw + vw / 2, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_RIGHT:
            return hsw + vw / 2, 0, 0
        elif self == DependantPosition.OUT_BOTTOM_RIGHT:
            position = hsw + vw / 2, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_BOTTOM:
            position = 0, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_BOTTOM_LEFT:
            position = -hsw - vw / 2, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_LEFT:
            position = -hsw - vh / 2, 0, 0
        elif self == DependantPosition.QUADRANT_1_TOP_RIGHT_CORNER:
            position = -vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position = -vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position = -hsw + vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_TOP_LEFT_CORNER:
            position = vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position = hsw - vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position = vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_TOP_LEFT_CORNER:
            position = vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_TOP_RIGHT_CORNER:
            position = hsw - vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position = vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_TOP_LEFT_CORNER:
            position = -hsw + vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_TOP_RIGHT_CORNER:
            position = -vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position = -vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.RANDOM_INSIDE:
            position = DependantPosition.get_random_inside().get_manim_position_center((vw, vh))
        elif self == DependantPosition.RANDOM_OUTSIDE:
            position = DependantPosition.get_random_outside().get_manim_position_center((vw, vh))

        return position
    
# TODO: These 2 methods below are similar to the ones in
# yta_multimedia\video\edition\effect\moviepy\position\objects\coordinate.py
def is_size_valid(size: tuple):
    """
    Check if the provided 'size' is a valid value or not.
    """
    if not PythonValidator.is_tuple(size) or len(size) != 2 or not NumberValidator.is_number_between(size[0], 1, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(size[1], 1, NORMALIZATION_MAX_VALUE):
        return False
    
    return True

def validate_size(size: tuple, parameter_name: str):
    """
    Validate the provided 'size' and raises an Exception if
    not valid.
    """
    if not is_size_valid(size):
        raise Exception(f'The provided {parameter_name} parameter is not a tuple or does not have 2 elements that are numbers between 1 and {str(NORMALIZATION_MAX_VALUE)}.')