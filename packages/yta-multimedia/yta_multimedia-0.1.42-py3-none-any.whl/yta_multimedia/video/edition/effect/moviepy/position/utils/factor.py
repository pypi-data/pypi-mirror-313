"""
This module is to encapsulate some factor calculations
to make easy building new effects.
"""
from typing import Union
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_general_utils.programming.parameter_validator import PythonValidator


def get_factor_to_fit_area(area: tuple, scene_size: tuple = (1920, 1080)):
    """
    This method calculates the factor we need to apply to the
    resize method to obtain a video in which the provided 
    'area' is displayed fitting the whole scene with its
    center in the middle of it.
    """
    # TODO: Maybe improve validations
    if not PythonValidator.is_tuple(area) or len(area) != 2:
        raise Exception('The provided "area" parameter is not a tuple of 2 values.')

    if not PythonValidator.is_tuple(scene_size) or len(scene_size) != 2:
        raise Exception('The provided "scene_size" parameter is not a tuple of 2 values.')

    # We calculate the resize factor we need to make the
    # video fit only the area size
    factor = max(
        scene_size[0] / area[0],
        scene_size[1] / area[1]
    )

    return factor

def get_factor_to_fit_scene(video_position: Union[tuple, Coordinate, Position], position_in_scene: Union[tuple, Coordinate, Position], video_size: tuple, scene_size: tuple = (1920, 1080)):
    """
    This method calculates the factor we need to apply to the
    resize method to obtain a video that fits the scene without
    any black region.
    """
    if not PythonValidator.is_instance(video_position, [Position, Coordinate]):
        if not PythonValidator.is_instance(video_position, tuple) and len(video_position) != 2:
            raise Exception('Provided "video_position" is not a valid Position enum or (x, y) tuple.')
        else:
            video_position = Coordinate(video_position[0], video_position[1])
        
    if not PythonValidator.is_instance(position_in_scene, [Position, Coordinate]):
        if not PythonValidator.is_instance(position_in_scene, tuple) and len(position_in_scene) != 2:
            raise Exception('Provided "position_in_scene" is not a valid Position enum or (x, y) tuple.')
        else:
            position_in_scene = Coordinate(position_in_scene[0], position_in_scene[1])

    # TODO: Improve this by checking that is about positive values
    if not PythonValidator.is_tuple(video_size) or len(video_size) != 2:
        raise Exception('The provided "video_size" is not a valid size.')
    
    if not PythonValidator.is_tuple(scene_size) or len(scene_size) != 2:
        raise Exception('The provided "scene_size" is not a valid size.')
    
    # We need to calculate the difference in size between the 
    # scene size and the video size with the new position as
    # its center to be able to calculate the factor later that
    # we need to apply to resize the video to fit the actual
    # scene size and avoid any black region
    factor = max(
        scene_size[0] / (video_size[0] - abs(position_in_scene.get_moviepy_center_tuple()[0] - video_position.x) * 2),
        scene_size[1] / (video_size[1] - abs(position_in_scene.get_moviepy_center_tuple()[1] - video_position.y) * 2)
    )

    return factor