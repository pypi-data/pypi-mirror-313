from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWithPrecalculated
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video import VideoHandler
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.position.utils.factor import get_factor_to_fit_scene, get_factor_to_fit_area
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.Clip import Clip
from typing import Union


class ZoomOutOnVideoPositionEffect(Effect):
    """
    Creates a Zoom using a specific position of the video
    as its center to make the zoom effect on it. This 
    effect will adapt the video size to fit the full scene
    size and avoid showing any black area.
    """
    def apply(cls, video: Clip, video_position: Union[tuple, Coordinate, Position], zoom_start_region_size: tuple, rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'. The 'video_position'
        parameter is the position (within the video) we want to use as
        the new center. This effect will place the center of the
        provided 'video' in the Position.CENTER position (center of 
        the scene).
        """
        # TODO: What about 'rate_func' (?)
        video = VideoParser.to_moviepy(video)

        if not PythonValidator.is_instance(video_position, [Position, Coordinate]):
            if not PythonValidator.is_instance(video_position, tuple) and len(video_position) != 2:
                raise Exception('Provided "video_position" is not a valid Position enum or (x, y) tuple.')
            else:
                video_position = Coordinate(video_position[0], video_position[1])

        if not PythonValidator.is_tuple(zoom_start_region_size) or len(zoom_start_region_size) != 2:
            raise Exception('The provided "zoom_start_region_size" parameter is not a valid tuple of 2 values.')
            
        # TODO: This is actually written in another part of the code
        # and maybe I can make it dynamic depending on the actual
        # background (scene) size, but by now here it is to make it 
        # work
        MAX_SCENE_SIZE = (1920, 1080)
        # We force Position.CENTER because any other thing doesn't
        # make sense at all (at least by now), but I can set it as
        # a parameter
        POSITION_IN_SCENE = Position.CENTER

        resize_factor = get_factor_to_fit_area(zoom_start_region_size, MAX_SCENE_SIZE)

        video_handler = VideoHandler(video)
        resizes = [
            TFunctionResize.resize_from_to(t, video.duration, resize_factor, 1, RateFunction.linear) for t in video_handler.frame_time_moments
        ]

        # We usually use the center of the video to manipulate it
        # and to place that center in the position in which we 
        # want to place it, because that is how it should be done
        # to be able to place it later
        video_center_difference = (
            video.w / 2 - video_position.x,
            video.h / 2 - video_position.y
        )

        positions = [
            POSITION_IN_SCENE.get_moviepy_upper_left_corner_tuple((
                # TODO: Maybe I need to apply a rate_func here to make
                # it non-linear
                (video.w - video_center_difference[0] * 2 * (1 - i / len(resizes))) * resizes[i],
                (video.h - video_center_difference[1] * 2 * (1 - i / len(resizes))) * resizes[i]
            )) for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply(video, with_position_list = positions, resized_list = resizes)

    def apply_over_video():
        pass
    # TODO: 'apply_over_video' here (?)

    # TODO: I want to keep this code below because it is another
    # way of building the video animation. This code below makes
    # a zoom out using not the whole video but only the size
    # that makes, with the coordinate still on the center of the 
    # scene, fit the maximum video size without showing black
    # borders
    def test(cls, video: Clip, video_position: Union[tuple, Coordinate, Position], position_in_scene: Union[tuple, Coordinate, Position], rate_func: type = RateFunction.linear):
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

        # We usually use the center of the video to manipulate it
        # and to place that center in the position in which we 
        # want to place it, because that is how it should be done
        # to be able to place it later
        video_center_difference = (
            video.w / 2 - video_position.x,
            video.h / 2 - video_position.y
        )

        positions = [
            position_in_scene.get_moviepy_upper_left_corner_tuple((
                (video.w - video_center_difference[0] * 2) * resizes[i],
                (video.h - video_center_difference[1] * 2) * resizes[i]
            )) for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply(video, with_position_list = positions, resized_list = resizes)