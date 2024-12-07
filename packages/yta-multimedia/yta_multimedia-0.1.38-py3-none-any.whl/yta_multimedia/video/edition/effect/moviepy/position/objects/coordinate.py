from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH, STANDARD_HEIGHT, STANDARD_WIDTH
from yta_general_utils.coordinate.coordinate import Coordinate as BaseCoordinate
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import PythonValidator
from typing import Union
from copy import copy


class VideoEngine(Enum):
    """
    Enum class to represent the different video engine
    systems we are using in this app.
    """
    MOVIEPY = 'moviepy'
    """
    The moviepy video engine which uses the upper left
    corner as the origin of the movement and has a scene
    which origin (0, 0) is the upper left corner, being
    positive values bottom and right directions and 
    negative top and left.
    """
    MANIM = 'manim'
    """
    The manim video engine which uses the center of the
    video as the origin of the movement and has a scene
    which origin (0, 0) is in the middle being positive
    values top and right directions and negative bottom
    and left.
    """

class Coordinate(BaseCoordinate):
    """
    Class that represents a position in a scene with
    of specific dimensions. This class will always
    refer to the center of the element positioned in
    that position.

    This class contains method to calculate the corner
    of the element to be able to move moviepy videos,
    but it is always pointing to the center of the 
    element.
    """
    engine: VideoEngine = None
    """
    The video engine for which this coordinate has
    been created.
    """
    scene_size: tuple = None
    """
    The scene dimensions (for moviepy engine) the
    coordinate has been built for.
    """

    def __init__(self, x: float, y: float, is_normalized: bool = False, engine: Union[VideoEngine, str] = VideoEngine.MOVIEPY, scene_size: tuple = (1920, 1080)):
        super().__init__(x, y, is_normalized)
        engine = VideoEngine.to_enum(engine)

        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            super().validate(scene_size, 'scene_size')
        
        self.type = type
        self.engine = engine
        self.scene_size = scene_size

    def to_moviepy(self):
        """
        This method updates the instance 'x', 'y' and 'engine'
        values if the current engine is Manim. If this happens,
        the scene will be set as (1920, 1080), as this is the
        default scene we consider for manim.
        """
        if self.engine == VideoEngine.MANIM:
            new_coordinate = self.as_moviepy_tuple()

            self.x = new_coordinate[0]
            self.y = new_coordinate[1]
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we force it
            self.scene_size = (1920, 1080)
            self.engine = VideoEngine.MOVIEPY

        return self
    
    def to_manim(self):
        """
        This method updates the instance 'x', 'y' and 'engine'
        values if the current engine is Moviepy. If this happens,
        the scene will be set as (1920, 1080), as this is the
        default scene we consider for moviepy.
        """
        if self.engine == VideoEngine.MOVIEPY:
            new_coordinate = self.as_manim_tuple()

            self.x = new_coordinate[0]
            self.y = new_coordinate[1]
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we force it
            self.scene_size = (1920, 1080)
            self.engine = VideoEngine.MANIM

        return self

    def as_moviepy_tuple(self):
        """
        Return this Coordinate instance as a moviepy coordinate
        tuple. This method will return a value but not update
        any instance attribute.

        This method forces the scene to be (1920, 1080) that
        is the default scene size (in normal size terms).
        """
        x, y = self.x, self.y
        if self.engine == VideoEngine.MANIM:
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we need to make sure
            # it is refering that screen size.
            # TODO: I need to refactor this. When 'x' is 0
            # in moviey in a 1920x1080 scene, the manim value
            # would be -
            x, y = self.on_scene_size((1920, 1080))
            x, y = Coordinate.manim_coordinate_to_moviepy_coordinate((x, y))

        return x, y
    
    def as_manim_tuple(self):
        """
        Return this Coordinate instance as a manim coordinate
        tuple. This method will return a value but not update
        any instance attribute.

        This method forces the scene to be (1920, 1080) that
        is the default scene size (in normal size terms).
        """
        x, y = self.x, self.y
        if self.engine == VideoEngine.MOVIEPY:
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we need to make sure
            # it is refering that screen size.
            x, y = self.on_scene_size((1920, 1080))
            x, y = Coordinate.moviepy_coordinate_to_manim_coordinate((x, y))

        return x, y

    def update_scene_size(self, scene_size: tuple = (1920, 1080)):
        """
        Update the current scene size and also the coordinate
        values to fit the new scene size. This method updates
        this Coordiante instance attributes.
        """
        x, y = self.on_scene_size(scene_size)

        # TODO: What if Manim (?)
        self.x = x
        self.y = y
        self.scene_size = scene_size

        return self
    
    def on_scene_size(self, scene_size: tuple = (1920, 1080)):
        """
        Obtain the 'x' and 'y' values that fit the provided 
        'scene_size' by making the required calculations.

        This method do not modify the instance.
        """
        super().validate(scene_size, 'scene_size')

        x, y = self.x, self.y
        if self.scene_size != scene_size:
            tmp: Coordinate = copy(self)
            tmp = tmp.update_scene_size(scene_size)
            x, y = tmp.x, tmp.y
        
        return x, y

    def get_moviepy_upper_left_corner_tuple(self, video_size: tuple):
        """
        Calculate the upper left corner tuple of this Coordinate
        instance based on its screen_size and the provided
        'video_size'.
        """
        super().validate(video_size, 'video_size')

        # TODO: What if Manim (?)
        if self.engine == VideoEngine.MANIM:
            raise Exception('Please, write the code for this.')

        return self.x - video_size[0] / 2, self.y - video_size[1] / 2
    
    @staticmethod
    def to_moviepy_upper_left_corner_tuple(coordinate: Union[tuple, 'Coordinate'], video_size: Union[tuple, 'Coordinate'], scene_size: Union[tuple, 'Coordinate'] = (1920, 1080)):
        """
        Calculate the upper left corner using the provided
        'coordinate', 'video_size' and making the calculations
        based on a scene of the provided 'scene_size'.
        """
        super().validate(coordinate, 'coordinate')
        super().validate(video_size, 'video_size')
        super().validate(scene_size, 'scene_size')

        if PythonValidator.is_instance(coordinate, Coordinate):
            # TODO: What about manim (?)
            # TODO: Is this updating the reference?, If yes,
            # that is an unexpected behaviour
            #coordinate = coordinate.update_scene_size(scene_size)
            tmp: Coordinate = copy(coordinate)
            tmp = tmp.update_scene_size(scene_size)
        else:
            coordinate = Coordinate(coordinate[0], coordinate[1], scene_size = scene_size)

        return coordinate.get_moviepy_upper_left_corner_tuple(video_size)
    
    @staticmethod
    def moviepy_coordinate_to_manim_coordinate(coordinate: tuple):
        """
        Transform the provided moviepy 'coordinate' to
        a manim coordinate. Each of those coordinates 
        must be considered as built in a 1920x1080 scene.

        Please, ensure the provided 'coordinate' is 
        representing a point within a scene of 1920x1080.
        """
        super().validate(coordinate)

        # Scale for moviepy -> manim conversion
        x_scale = (HALF_SCENE_WIDTH * 2) / STANDARD_WIDTH
        y_scale = (HALF_SCENE_HEIGHT * 2) / STANDARD_HEIGHT
        
        x = (coordinate[0] - STANDARD_WIDTH / 2) * x_scale
        y = (STANDARD_HEIGHT / 2 - coordinate[1]) * y_scale

        return x, y
    
    @staticmethod
    def manim_coordinate_to_moviepy_coordinate(coordinate: tuple):
        """
        Transform the provided manim 'coordinate' to
        a moviepy coordinate. Each of those coordinates 
        must be considered as built in a 1920x1080 scene.

        Please, ensure the provided 'coordinate' is 
        representing a point within a scene of 1920x1080.
        """
        super().validate(coordinate)

        # Escala para Manim -> MoviePy (inversa)
        x_scale = STANDARD_WIDTH / (HALF_SCENE_WIDTH * 2)
        y_scale = STANDARD_HEIGHT / (HALF_SCENE_HEIGHT * 2)
        
        # Conversión de Manim a MoviePy
        x = (coordinate[0] * x_scale) + HALF_SCENE_WIDTH
        y = HALF_SCENE_HEIGHT - (coordinate[1] * y_scale)

        return x, y

    @staticmethod
    def to_coordinate(coordinate: tuple):
        super().validate(coordinate)

        return Coordinate(coordinate[0], coordinate[1])