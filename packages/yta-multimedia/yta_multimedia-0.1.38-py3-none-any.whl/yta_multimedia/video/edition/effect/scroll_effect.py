from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from moviepy import Clip
from moviepy.video.fx import Scroll


class ScrollEffect(Effect):
    """
    This effect will make the clip be scrolled like if a zoomed
    region was surfing through the clip.
    """

    def apply(self, video: Clip, width = None, height = None, x_speed = None, y_speed = None, x_start = None, y_start = None) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        width = width if width else video.w / 2
        height = height if height else video.h / 2
        # TODO: Make these params below dynamic
        x_speed = x_speed if x_speed else 20
        y_speed = y_speed if y_speed else 20
        x_start = x_start if x_start else 0
        y_start = y_start if y_start else 0

        return Scroll(width, height, x_speed, y_speed, x_start, y_start)