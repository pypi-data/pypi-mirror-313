from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.color import Color, ColorString
from moviepy import Clip
from moviepy.video.fx import FadeIn as MoviepyFadeIn
from typing import Union


class FadeInEffect(Effect):
    """
    This effect will make the video appear progressively
    lasting the provided 'duration' time or the whole 
    clip duration if None 'duration' provided.

    The 'color' provided must be a valid color string, 
    array, tuple or Color instance, or will be set as 
    pure black if None provided.
    """
    def apply(self, video: Clip, duration: float, color: Union[list, tuple, str, Color] = None) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        duration = duration if duration is not None else video.duration
        color = Color.parse(color).as_rgb_array() if color is not None else Color.parse(ColorString.BLACK).as_rgb_array()

        return MoviepyFadeIn(duration, color).apply(video)