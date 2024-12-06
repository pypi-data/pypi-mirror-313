from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy.video.fx import MultiplySpeed
from moviepy import Clip


class FitDurationEffect(Effect):
    """
    This effect changes the speed of the video to fit
    the requested 'duration', that will accelerate
    or decelerate the video speed.
    """
    def apply(self, video: Clip, duration: float = None) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        if not NumberValidator.is_number_between(duration, 0, 120, False):
            raise Exception(f'The provided "duration" parameter "{str(duration)}" is not a valid number between 0 (not included) and 120 (included).')

        return MultiplySpeed(final_duration = duration).apply(video)
    
# TODO: Maybe I can create another effect to set
# the speed by multiplying it by a factor, but 
# by now this one is enough