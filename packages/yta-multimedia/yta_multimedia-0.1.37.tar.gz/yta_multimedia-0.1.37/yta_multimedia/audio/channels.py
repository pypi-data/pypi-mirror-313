from yta_multimedia.audio.parser import AudioParser
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.filename import filename_is_type, FileType, replace_file_extension, get_file_extension
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip

from typing import Union


class AudioChannel(Enum):
    LEFT = 1
    RIGHT = 0

# TODO: Refactor this and move to a class
def isolate_audio_channel(audio, channel: AudioChannel = AudioChannel.LEFT, output_filename: Union[str, None] = None):
    """
    Gets the provided 'audio' and isolates it to he given 'channel' onlye (that can
    be left or right). It will be stored as a local file if 'output_filename' 
    provided, and will return the new isolated audio as a pydub AudioSegment.
    """
    audio = AudioParser.to_audiosegment(audio)
    channel = AudioChannel.to_enum(channel)

    channel_pan = -1.0
    if AudioChannel == AudioChannel.RIGHT:
        channel_pan = 1.0
    
    audio = adjust_audio_channels(audio, channel_pan, None, 0, audio.duration_seconds * 1000)

    if output_filename:
        if not filename_is_type(output_filename, FileType.AUDIO):
            replace_file_extension(output_filename, '.wav')

        audio.export(out_f = output_filename, format = get_file_extension(output_filename))

    return audio

def apply_8d_effect(audio):
    """
    Generates a 8d sound effect by splitting the 'audio'' into multiple 
    smaller pieces, pans each piece to make the sound source seem like 
    it is moving from L to R and R to L in loop, decreases volume towards
    center position to make the movement sound like it is a circle 
    instead of straight line.
    """
    audio = AudioParser.to_audiosegment(audio)

    SCREEN_SIZE = 1920
    NUM_OF_PARTS = 80
    AUDIO_PART_SCREEN_SIZE = SCREEN_SIZE / NUM_OF_PARTS
    AUDIO_PART_TIME = audio.duration_seconds * 1000 / NUM_OF_PARTS

    cont = 0
    while ((cont * AUDIO_PART_TIME) < audio.duration_seconds * 1000):
        coordinate = cont * AUDIO_PART_SCREEN_SIZE
        channel_pan = x_coordinate_to_channel_pan(coordinate)
        volume_adjustment = 5 - (abs(channel_pan) / NUM_OF_PARTS) * 5

        start_time = cont * AUDIO_PART_TIME
        end_time = (cont + 1) * AUDIO_PART_TIME
        # I do this because of a small error that makes it fail
        if end_time > audio.duration_seconds * 1000:
            end_time = audio.duration_seconds * 1000
        audio = adjust_audio_channels(audio, channel_pan, volume_adjustment, start_time, end_time)
        cont += 1

    return audio

def x_coordinate_to_channel_pan(x: int):
    """
    This method calculates the corresponding channel pan value (between -1.0 and
    1.0) for the provided "x" coordinate (in an hypotetic scene of 1920x1080).
    This means that an "x" of 0 will generate a -1.0 value, and an "x" of 1919
    will generate a 1.0 value. Values out of limits (lower than 0 or greater
    than 1919) will be set as limit values (0 and 1919).

    This method has been created to be used in transition effects sounds, to be
    dynamically panned to fit the element screen position during the movement.
    """
    if not x and x != 0:
        raise Exception('No "x" provided.')
    
    if x < 0:
        x = 0

    if x > 1919:
        x = 1919

    return -1.0 + (x * 2.0 / 1919)

def adjust_audio_channels(audio, channel_pan: float = 0.0, volume_gain: float = 1.0, start_time = None, end_time = None):
    """
    This method allows you to set the amount of 'audio' you want to be
    sounding on each of the 2 channels (speakers), right and left. The
    'channel_pan' parameter must be a value between -1.0, which means
    left channel, and 1.0, that means right channel. A value of 0 means
    that the sound will sound equally in left and right channel. A value
    of 0.5 means that it will sound 25% in left channel and 75% in right
    channel.

    The 'volume_gain', if 0, puts the fragment in silence. If 1, it has
    the same volume. If 2, the volume is twice.

    This method will apply the provided 'channel_pan' to the also provided
    'audio'. The 'start_time' and 'end_time' parameters determine the part
    of the audio you want the channel panning to be applied, and it is in
    seconds.
    """
    audio = AudioParser.to_audiosegment(audio)

    if not channel_pan:
        raise Exception('No "channel_pan" provided.')

    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be a value between -1.0 and 1.0.')
    
    # TODO: Check that 'volume_adjustment' is a number, not only a float
    if volume_gain and not isinstance(volume_gain, float) and not isinstance(volume_gain, int):
        raise Exception('The "volume_gain" parameter must be a valid number.')
    
    if not start_time:
        start_time = 0

    if not end_time:
        end_time = audio.duration_seconds * 1000

    if start_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if start_time > audio.duration_seconds * 1000:
        raise Exception('The "start_time" cannot be greater than the actual "audio" duration.')
    
    if start_time > end_time:
        raise Exception('The "start_time" cannot be greater than the "end_time".')
    
    if end_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if end_time > audio.duration_seconds * 1000:
        raise Exception('The "end_time" cannot be greater than the actual "audio" duration.')
    
    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be between -1.0 (left) and 1.0 (right)')

    # Process the part we want
    modified_part = audio[start_time: end_time]
    if volume_gain < 1:
        # We minimize the audio (x3) if lower to 1
        modified_part -= abs(modified_part.dBFS * (1 - volume_gain) * 3)
    else:
        modified_part += abs(modified_part.dBFS * (volume_gain - 1))
    modified_part = modified_part.pan(channel_pan)

    if start_time == 0 and end_time == audio.duration_seconds * 1000:
        audio = modified_part
    elif start_time == 0:
        audio = modified_part + audio[end_time: audio.duration_seconds * 1000]
    elif end_time == audio.duration_seconds * 1000:
        audio = audio[0: start_time] + modified_part
    else:
        audio = audio[0: start_time] + modified_part + audio[end_time: audio.duration_seconds * 1000]

    return audio

def get_audio_synchronized_with_video_by_position(audio, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
    """
    This method iterates over the whole provided 'video' and uses its
    position in each frame to synchronize that position with the also
    provided 'audio' that will adjust its pan according to it.

    This method returns the audio adjusted as a pydub AudioSegment.
    """
    audio = AudioParser.to_audiosegment(audio)
    video = VideoParser.to_moviepy(video)

    frames_number = int(video.fps * video.duration)
    frame_duration = video.duration / frames_number

    # I need to know the minimum x below 0 and the maximum above 1919
    minimum_x = 0
    maximum_x = 1919
    for i in range(frames_number):
        t = frame_duration * i
        # We want the center of the video to be used
        video_x = video.pos(t)[0] + video.w / 2
        if video_x < 0 and video_x < minimum_x:
            minimum_x = video_x
        if video_x > 1919 and video_x > maximum_x:
            maximum_x = video_x

    for i in range(frames_number):
        t = frame_duration * i
        video_x = video.pos(t)[0] + video.w / 2

        # I want to make it sound always and skip our exception limits
        volume_gain = 1
        if video_x < 0:
            volume_gain -= abs(video_x / minimum_x)
            video_x = 0
        elif video_x > 1919:
            volume_gain -= abs((video_x - 1919) / (maximum_x - 1919))
            video_x = 1919

        audio = adjust_audio_channels(audio, x_coordinate_to_channel_pan(video_x), volume_gain, t * 1000, (t + frame_duration) * 1000)

    return audio

def synchronize_audio_pan_with_video_by_position(audio, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
    """
    This method synchronizes the provided 'video' with the also provided
    'audio' by using its position to adjust the pan.

    This method returns the provided 'video' with the new audio 
    synchronized.
    """
    video = video.with_audio(AudioParser.to_audiofileclip(get_audio_synchronized_with_video_by_position(audio, video)))

    return video