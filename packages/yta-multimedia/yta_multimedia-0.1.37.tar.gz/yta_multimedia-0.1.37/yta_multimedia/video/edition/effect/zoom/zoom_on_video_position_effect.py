from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWithPrecalculated
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video import VideoHandler
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.Clip import Clip
from typing import Union

import numpy as np

# TODO: Rename it, as it is making zoom but in an
# specific an static position, so it should be
# something like ZoomInPlaceEffect
class ZoomOnVideoPositionEffect(Effect):
    """
    Creates a Zoom using a specific position of the video
    as its center to make the zoom effect on it. This 
    effect will adapt the video size to fit the scene and
    avoid showing any black area.
    """
    def apply(cls, video: Clip, video_position: Union[tuple, Coordinate, Position], position_in_scene: Union[tuple, Coordinate, Position], rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'.
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

        # Calculate new 'center' of the video
        x_distance_from_actual_center_to_new_center = (video.w // 2) - video_position.x
        y_distance_from_actual_center_to_new_center = (video.h // 2) - video_position.y

        # We need to calculate the distance between the scene position
        # in which we are placing the video and the actual position
        # (within the video) that we are using as the new center
        dawx = abs(position_in_scene.get_moviepy_center_tuple()[0] - video_position.x)
        dawy = abs(position_in_scene.get_moviepy_center_tuple()[1] - video_position.y)

        # TODO: This is actually written in another part of the code
        # and maybe I can make it dynamic depending on the actual
        # background (scene) size, but by now here it is to make it 
        # work
        MAX_SCENE_SIZE = (1920, 1080)

        # We need to calculate the maximum resize factor needed to make
        # the video fit the full screen size
        min_resize_factor = max(MAX_SCENE_SIZE[0] / (video.w - dawx * 2), MAX_SCENE_SIZE[1] / (video.h - dawy * 2))

        video_handler = VideoHandler(video)
        #gsvideo = gsvideo.resized(min_resize_factor)
        # This 1.5 is the static zoom factor we are using now but it
        # is only for this zoom. Make it dynamic later
        resizes = [
            TFunctionResize.resize_from_to(t, video.duration, min_resize_factor * 1.5, min_resize_factor, RateFunction.linear) for t in video_handler.frame_time_moments
        ]

        positions = [
            position_in_scene.get_moviepy_upper_left_corner_tuple((
                video.w * resizes[i] - x_distance_from_actual_center_to_new_center * resizes[i] * 2,
                video.h * resizes[i] - y_distance_from_actual_center_to_new_center * resizes[i] * 2
            )) for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply(video, with_position_list = positions, resized_list = resizes)

    # TODO: 'apply_over_video' here (?)