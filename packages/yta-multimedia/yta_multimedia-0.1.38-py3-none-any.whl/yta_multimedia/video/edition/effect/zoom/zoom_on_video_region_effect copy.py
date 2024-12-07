from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWithPrecalculated
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video import VideoHandler
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.position.utils.factor import get_factor_to_fit_region, get_factor_to_fit_scene
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.image.region.image_region import ImageRegion
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.Clip import Clip
from typing import Union

import numpy as np

# TODO: Rename it, as it is making zoom but in an
# specific an static position, so it should be
# something like ZoomInPlaceEffect
class ZoomOnVideoRegionEffect(Effect):
    """
    Creates a Zoom using a specific position of the video
    as its center to make the zoom effect on it. This 
    effect will adapt the video size to fit the full scene
    size and avoid showing any black area.
    """
    def apply(cls, video: Clip, region: ImageRegion, rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'.
        """
        # TODO: What about 'rate_func' (?)
        video = VideoParser.to_moviepy(video)

        if not PythonValidator.is_instance(region, ImageRegion):
            raise Exception('The provided "region" is not a valid ImageRegion class instance.')

        # TODO: This is actually written in another part of the code
        # and maybe I can make it dynamic depending on the actual
        # background (scene) size, but by now here it is to make it 
        # work
        MAX_SCENE_SIZE = (1920, 1080)
        # TODO: This could be dynamic
        position_in_scene = Position.CENTER

        factor_to_fit_region_size = get_factor_to_fit_region(region, MAX_SCENE_SIZE)

        # TODO: If I get the 'resize_factor_to_fit_scene' I can
        # make an animation from region fitting to scene fitting
        factor_to_fit_scene_size = get_factor_to_fit_scene(region.center, position_in_scene, (video.w, video.h), MAX_SCENE_SIZE)

        video_handler = VideoHandler(video)
        # We make the video go to fitting region to fit the
        # whole scene size (without black reigons)
        resizes = [
            TFunctionResize.resize_from_to(t, video.duration, factor_to_fit_region_size, factor_to_fit_scene_size, RateFunction.linear) for t in video_handler.frame_time_moments
        ]

        # Calculate new differente between the real center 
        # and the new center of the video
        video_center_difference = (
            video.w - region.center[0] * 2,
            video.h - region.center[y] * 2
        )

        positions = [
            position_in_scene.get_moviepy_upper_left_corner_tuple((
                (video.w - video_center_difference[0]) * resizes[i],
                (video.h - video_center_difference[1]) * resizes[i]
            )) for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply(video, with_position_list = positions, resized_list = resizes)

    # TODO: 'apply_over_video' here (?)