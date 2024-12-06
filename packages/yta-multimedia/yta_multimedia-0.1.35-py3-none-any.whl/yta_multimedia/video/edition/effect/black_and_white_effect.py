from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from moviepy import Clip
from moviepy.video.fx import BlackAndWhite


class BlackAndWhiteEffect(Effect):
    """
    This effect will make the clip appear in black and
    white colors.
    """
    def apply(self, video: Clip) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        return BlackAndWhite().apply(video)