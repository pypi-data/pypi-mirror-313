from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.fade_out_effect import FadeOutEffect
from yta_multimedia.video.edition.effect.fade_in_effect import FadeInEffect
from yta_general_utils.color import Color, ColorString
from moviepy import Clip, concatenate_videoclips
from typing import Union


class BlinkEffect(Effect):
    """
    This method makes the provided video blink, that is a composition of
    a FadeOut and a FadeIn consecutively to build this effect. The duration
    will be the whole clip duration. The FadeIn will last the half of the
    clip duration and the FadeOut the other half.

    The 'color' parameter is the color you want for the blink effect as the
    background color. The default value is black ([0, 0, 0]).
    """
    def apply(self, video: Clip, color: Union[list, tuple, str, Color] = None) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        color = Color.parse(color).as_rgb_array() if color is not None else Color.parse(ColorString.BLACK).as_rgb_array()

        half_duration = video.duration / 2
        video = concatenate_videoclips([
            FadeOutEffect().apply(video.with_subclip(0, half_duration), half_duration, color),
            FadeInEffect().apply(video.with_subclip(half_duration, video.duration), half_duration, color)
        ])

        return video