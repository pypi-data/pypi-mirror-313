from yta_multimedia.video.parser import VideoParser
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from moviepy.Effect import Effect
from moviepy.Clip import Clip
from moviepy import concatenate_videoclips
from abc import abstractmethod


class MEffect(Effect):
    """
    Effect to be applied on a single video without any
    other video dependence.

    This effect cannot be applied as moviepy effects as
    the structure is different.

    TODO: If I want to make my own moviepy effects that
    are able to be applied as moviepy does, I need to
    respect the structure and just manipulate the frames.
    So, those new custom moviepy effects sohuld be placed
    in other folder as this MEffect is my own effect that
    works in a different way.
    """
    # TODO: Is this working (?)
    result_must_replace: bool = False
    """
    This parameter indicates if this effect, when applied,
    must replace the original clip part or, if False, must
    be concatenated.
    """
    @abstractmethod
    def apply_over_video(self, video: Clip, background_video: Clip):
        # TODO: Should I (?)
        pass

    @staticmethod
    def apply_effect_partially_on_video(video: Clip, effect: 'MEffect', start_time: float = 0, end_time: float = None):
        """
        Apply the provided 'effect' in the also provided 'video'
        in the part between the given 'start_time' and 'end_time'.
        """
        video = VideoParser.to_moviepy(video)

        # TODO: It will be a subclass of it, does it work (?)
        if not PythonValidator.is_instance(effect, MEffect):
            raise Exception('The provided "effect" parameter is not a valid effect. It must be an instance of MEffect class.')

        if not NumberValidator.is_number_between(start_time, 0, video.duration) or not NumberValidator.is_number_between(end_time, 0, video.duration) or start_time >= end_time:
            raise Exception('The provided "start_time" and "end_time" parameters ("{str(start_time)}" and "{str(end_time)}") must be values between 0 and the provided clip duration ("{str(video.duration)}"), and "end_time" must be greater than "start_time".')
        
        left = None if (start_time == 0) else video.with_subclip(0, start_time)
        # TODO: What if only '.apply()' instead of '.apply_over_video()'
        # is needed (?)
        center = effect.apply_over_video(video.with_subclip(start_time, end_time))
        right = None if (end_time is None) else video.with_subclip(start_time = end_time)

        clips = [clip for clip in [left, center, right] if clip is not None]

        return concatenate_videoclips(clips)#.with_start(start)