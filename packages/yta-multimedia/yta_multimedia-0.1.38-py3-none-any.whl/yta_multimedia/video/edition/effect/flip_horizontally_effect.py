from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from moviepy.video.fx import MirrorX
from moviepy import Clip


class FlipHorizontallyEffect(Effect):
    """
    This effect flips the video horizontally (including
    the mask).
    """
    def apply(self, video: Clip) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        return MirrorX().apply(video)