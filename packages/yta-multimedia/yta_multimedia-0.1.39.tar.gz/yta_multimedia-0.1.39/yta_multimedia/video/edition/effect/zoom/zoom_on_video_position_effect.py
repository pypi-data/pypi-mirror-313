from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWithPrecalculated
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video import VideoHandler
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.position.utils.factor import get_factor_to_fit_scene
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
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
    effect will adapt the video size to fit the full scene
    size and avoid showing any black area.
    """
    def apply(cls, video: Clip, video_position: Union[tuple, Coordinate, Position], position_in_scene: Union[tuple, Coordinate, Position], rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'. The 'video_position'
        parameter is the position (within the video) we want to use as
        the new center. The 'position_in_scene' is the position (within
        the scene) in which we want to place the new center of the
        provided 'video'.
        """
        # TODO: What about 'rate_func' (?)
        video = VideoParser.to_moviepy(video)

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

        # TODO: This is actually written in another part of the code
        # and maybe I can make it dynamic depending on the actual
        # background (scene) size, but by now here it is to make it 
        # work
        MAX_SCENE_SIZE = (1920, 1080)

        resize_factor = get_factor_to_fit_scene(video_position, position_in_scene, (video.w, video.h), MAX_SCENE_SIZE)

        video_handler = VideoHandler(video)
        #gsvideo = gsvideo.resized(min_resize_factor)
        # TODO: This 1.5 is the static zoom factor we are using
        # now but it is only for this zoom. Make it dynamic later
        resizes = [
            TFunctionResize.resize_from_to(t, video.duration, resize_factor * 1.5, resize_factor, RateFunction.linear) for t in video_handler.frame_time_moments
        ]

        # Calculate new differente between the real center 
        # and the new center of the video
        video_center_difference = (
            video.w - video_position.x * 2,
            video.h - video_position.y * 2
        )

        positions = [
            position_in_scene.get_moviepy_upper_left_corner_tuple((
                (video.w - video_center_difference[0]) * resizes[i],
                (video.h - video_center_difference[1]) * resizes[i]
            )) for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply(video, with_position_list = positions, resized_list = resizes)

    # TODO: 'apply_over_video' here (?)