
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.generation import generate_video_from_image
from yta_multimedia.video.edition.effect.fit_duration_effect import FitDurationEffect
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy import VideoClip, concatenate_videoclips
from typing import Union


# TODO: Move this to a better place
class ExtendVideoMode(Enum):
    """
    This is a Enum to set the parameter option to extend the video
    duration with one of these modes (strategies).
    """
    LOOP = 'loop'
    """
    This mode will make the video loop (restart from the begining)
    until it reaches the expected duration.
    """
    FREEZE_LAST_FRAME = 'freeze_last_frame'
    """
    This mode will freeze the last frame of the video and extend 
    it until it reaches the expected duration.
    """
    SLOW_DOWN = 'slow_down'
    """
    This mode will change the speed of the provided video to make
    it fit the needed duration by deccelerating it. As you should
    know, this method changes the whole video duration so the 
    result could be unexpected. Use it carefully.
    """

class EnshortVideoMode(Enum):
    """
    This is a Enum to set the parameter option to enshort
    the video duration with one of these modes (strategies).
    """
    CROP = 'crop'
    """
    This mode will make a subclip of the clip and remove
    the remaining part to fit the expected duration time.
    """
    SPEED_UP = 'speed_up'
    """
    This mode will change the speed of the clip by speeding
    it up. This is useful to make clips shorter when we need
    it, but be careful when you use it. Could be a good 
    choice for transitions that you need to apply in a
    specific amount of time.
    """

def set_video_duration(video: Union[str, VideoClip], duration = float, extend_mode: ExtendVideoMode = ExtendVideoMode.LOOP, enshort_mode: EnshortVideoMode = EnshortVideoMode.CROP):
    """
    This method will return a copy of the provided 'video' with the desired
    'duration' by applying crops, loops or different strategies according
    to the provided 'extend_mode' and 'enshort_mode' parameters. If the
    provided 'duration' is lower than the actual 'video' duration, it will
    be shortened by applying the 'enshort_mode'. If it is greater, it will
    be extended until we reach the desired 'duration' by applying the 
    'extend_mode' provided.

    This method makes a 'video.copy()' internally to work and avoid problems
    with references.
    """
    video = VideoParser.to_moviepy(video)

    # TODO: Validate duration
    if not duration:
        raise Exception('No "duration" provided.')
    
    extend_mode = ExtendVideoMode.to_enum(extend_mode) if extend_mode is not None else ExtendVideoMode.default()
    enshort_mode = EnshortVideoMode.to_enum(enshort_mode) if extend_mode is not None else EnshortVideoMode.default()

    final_video = video.copy()

    if video.duration > duration:
        # We need to enshort it
        if enshort_mode == EnshortVideoMode.CROP:
            final_video = final_video.with_subclip(0, duration)
        elif enshort_mode == EnshortVideoMode.SPEED_UP:
            final_video = FitDurationEffect().apply(video, duration)
            #final_video = final_video.with_effects([MultiplySpeed(final_duration = duration)])
            # TODO: Remove this below when effects reviewed and
            # functionality is working perfectly
            #final_video = ChangeSpeedVideoEffect.apply(final_video, duration)
    elif video.duration < duration:
        # We need to enlarge it
        if extend_mode == ExtendVideoMode.LOOP:
            times_to_loop = (int) (duration / video.duration) - 1
            remaining_time = duration % video.duration
            for _ in range(times_to_loop):
                final_video = concatenate_videoclips([final_video, video])
            final_video = concatenate_videoclips([final_video, video.with_subclip(0, remaining_time)])
        elif extend_mode == ExtendVideoMode.FREEZE_LAST_FRAME:
            remaining_time = duration - video.duration
            frame = VideoFrameExtractor.get_frame_by_time(video, video.duration)
            frame_freezed_video = generate_video_from_image(frame, remaining_time)
            final_video = concatenate_videoclips([video, frame_freezed_video])
        elif extend_mode == ExtendVideoMode.SLOW_DOWN:
            final_video = FitDurationEffect().apply(video, duration)
            #final_video = final_video.with_effects([MultiplySpeed(final_duration = duration)])
            # TODO: Remove this below when effects reviewed and
            # functionality is working perfectly
            #final_video = ChangeSpeedVideoEffect.apply(final_video, duration)

    return final_video