from yta_multimedia.video.parser import VideoParser
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.temp import create_temp_filename
from moviepy import VideoClip
from typing import Union


def crop_video_using_key_frame_second(video: Union[VideoClip, str], key_frame_second: float = None, duration: float = None, output_filename: Union[str, None] = None):
    video = VideoParser.to_moviepy(video)

    # TODO: Refactor and review this below
    if not NumberValidator.is_number_between(key_frame_second, 0, video.duration):
        # We use the middle of the video as the key frame
        key_frame_second = video.duration / 2
    if not duration:
        duration = video.duration
    if duration > video.duration or duration <= 0:
        duration = video.duration

    if duration < video.duration:
        start_second = 0
        end_second = video.duration
        # Only if we have to crop it already
        half_duration = duration / 2
        if key_frame_second - half_duration < 0:
            # Start in 0.0
            start_second = 0
            end_second = duration
        elif key_frame_second + half_duration > video.duration:
            # End in 'video.duration'
            start_second = video.duration - duration
            end_second = video.duration
        else:
            # Use 'key_frame_second' as center
            start_second = key_frame_second - half_duration
            end_second = key_frame_second + half_duration

        video = video.with_subclip(start_second, end_second)

    if output_filename:
        # TODO: Check extension
        tmp_audiofilename = create_temp_filename('temp-audio.m4a')
        # TODO: Do I really need all those parameters?
        video.write_videofile(
            output_filename,
            codec = "libx264",
            temp_audiofile = tmp_audiofilename,
            remove_temp = True,
            audio_codec = 'aac' # pcm_s16le or pcm_s32le
        )

    return video