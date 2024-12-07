from yta_multimedia.video.parser import VideoParser
from yta_multimedia.audio.parser import AudioParser
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.temp import create_temp_filename
from moviepy import VideoClip, AudioClip
from typing import Union

import ffmpeg


def extract_audio_from_video(video: Union[VideoClip, str], output_filename: Union[str, None] = None):
    """
    Returns the audio in the video file provided as 'video_input'. If
    'output_filename' provided, it will write the audio in a file
    with that name.
    """
    video = VideoParser.to_moviepy(video)

    if output_filename:
        # TODO: Check extension, please
        video.audio.write_audiofile(output_filename)

    return video.audio

def set_audio_in_video(video: Union[VideoClip, str], audio: Union[AudioClip, str], output_filename: Union[str, None] = None):
    """
    This method returns a VideoFileClip that is the provided 'video_input' 
    with the also provided 'audio_input' as the unique audio (if valid
    parameters are provided). If 'output_filename' provided, it will
    write the video file with the new audio with that provided name.

    (!) If the input video file and the output file name are the same, you 
    will lose the original as it will be replaced.
    """
    video = VideoParser.to_moviepy(video)
    audio = AudioParser.to_audiofileclip(audio)

    video.audio = video.with_audio(audio)

    if output_filename:
        # TODO: Check extension, please
        # tmp_output_filename = create_temp_filename('tmp_output.mp4')

        # if variable_is_type(video_input, str) and variable_is_type(audio_input, str) and video_input and audio_input:
        #     # Both are valid str filenames, we will concat with ffmpeg
        #     # TODO: Check if I can get the original filename from an AudioFileClip|VideoFileClip
        #     ffmpeg.concat(ffmpeg.input(video_input), ffmpeg.input(audio_input), v = 1, a = 1).output(tmp_output_filename).run()
        # else:
        #     video_input.write_videofile(tmp_output_filename)
        #
        # rename_file(tmp_output_filename, output_filename, True)

        video.write_videofile(output_filename)

    return video

def set_audio_in_video_ffmpeg(video_filename: str, audio_filename: str, output_filename: str):
    """
    Sets the provided 'audio_filename' in the also provided 'video_filename'
    with the ffmpeg library and creates a new video 'output_filename' that
    is that video with the provided audio.

    TODO: This method need more checkings about extensions, durations, etc.
    """
    if not audio_filename or not FileValidator.file_is_audio_file(audio_filename) or not video_filename or not FileValidator.file_is_video_file(video_filename):
        raise Exception('The provided "audio_filename" and/or "video_filename" are not valid filenames.')
    
    if not output_filename:
        output_filename = create_temp_filename('tmp_audio_ffmpg.mp4')
    
    # TODO: What about longer audio than video (?)
    # TODO: Refactor this below with the FfmpegHandler
    input_video = ffmpeg.input(video_filename)
    input_audio = ffmpeg.input(audio_filename)

    ffmpeg.concat(input_video, input_audio, v = 1, a = 1).output(output_filename).run(overwrite_output = True)