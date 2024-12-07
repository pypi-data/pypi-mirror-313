from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math import Math
from moviepy import Clip, clips_array

import math


class MultipliedEffect(Effect):
    """
    Generates a clips array with the provided 'video' being shown
    'times' times (this parameter must be a pow of 4). This
    method has been created to be used internally with our own
    default methods.
    """
    def apply(self, video: Clip, times: int) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        if not times:
            times = 4
        else:
            if not Math.is_power_of_n(times, 4):
                raise Exception(f'The provided "times" parameter "{str(times)}" is not a power of 4.')

        audio = video.audio
        size = (video.w, video.h)

        # We build the matrix of sqrt(times, 2) videos
        # per row, and sqrt(times, 2) rows. So, if 16
        # 'times' provided, that is power of 4 and valid,
        # it will generate a 4x4 array. If 64 'times',
        # a 8x8 array that will be the composition
        items = int(math.sqrt(times))
        array = [[video] * items for _ in range(items)]

        return clips_array(array).resized(size).with_audio(audio)