from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.filters.frame import FrameFilter
from yta_multimedia.video.parser import VideoParser
from moviepy import Clip
from typing import Union


class BlurEffect(Effect):
    """
    This effect will blur the whole clip. The greater the
    'blur_radius' is, the more blurred it becomes.
    """
    def apply(self, video: Clip, blur_radius: Union[int, None] = None) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        blur_radius = blur_radius if blur_radius is not None else 4

        return video.transform(lambda get_frame, t: FrameFilter.blur(get_frame, t, blur_radius = blur_radius))