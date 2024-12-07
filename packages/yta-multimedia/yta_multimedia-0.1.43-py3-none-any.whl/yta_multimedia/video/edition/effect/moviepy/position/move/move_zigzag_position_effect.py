from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWith
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions import RateFunction
from moviepy.Clip import Clip
from typing import Union


class MoveZigzagPositionEffect(Effect):
    """
    Move from A to B doing a wave effect while moving.
    """
    # TODO: Is this working (?)
    result_must_replace = True

    def apply(cls, video: Union[Clip, str], initial_position: Union[Coordinate, Position], final_position: Union[Coordinate, Position]):
        video = VideoParser.to_moviepy(video)

        # TODO: Validate and parse 'initial_position' and 
        # 'final_position'. These positions must be coordinates
        # on a 1920x1080 scene.
        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.zigzag, RateFunction.linear)

        return MoviepyWith.apply(video, with_position = arg)
    
    def apply_over_video(cls, video: Union[Clip, str], background_video: Union[Clip, str], initial_position: Union[Coordinate, Position], final_position: Union[Coordinate, Position]):
        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.zigzag, RateFunction.linear)

        return MoviepyWith.apply_over_video(video, background_video, with_position = arg)