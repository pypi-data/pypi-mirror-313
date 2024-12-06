from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWith, MoviepyArgument
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_general_utils.math.rate_functions import RateFunction
from moviepy.Clip import Clip
from typing import Union


class ShakeDecreasingAtPositionEffect(Effect):
    def apply(self, video: Clip, position: Union[Position, Coordinate, tuple] = Position.CENTER) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        background_video = ClipGenerator.get_default_background_video()

        return self.apply_over_video(video, background_video, position)
    
    def apply_over_video(self, video: Clip, background_video: Clip, position: Union[Position, Coordinate] = Position.CENTER) -> Clip:
        arg = MoviepyArgument(position, position, TFunctionSetPosition.linear_with_decreasing_shaking, RateFunction.linear)

        return MoviepyWith().apply_over_video(video, background_video, with_position = arg)