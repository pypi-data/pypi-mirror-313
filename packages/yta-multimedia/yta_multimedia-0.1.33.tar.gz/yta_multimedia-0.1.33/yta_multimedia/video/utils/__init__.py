from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy import ImageClip
from yta_multimedia.video.parser import VideoParser
from typing import Union
import numpy as np


def generate_video_from_image(image, duration: float = 1, output_filename: Union[str, None] = None):
    """
    Receives an image and creates an ImageClip of 'duration' seconds.
    It will be also stored as a file if 'output_filename' is provided.
    """
    if not NumberValidator.is_positive_number(duration):
        raise Exception(f'The provided "duration" parameter {str(duration)} is not a positive number.')

    if not isinstance(image, ImageClip):
        video = ImageClip(ImageParser.to_numpy(image)).with_fps(60).with_duration(duration)

    if output_filename:
        video.write_videofile(output_filename)

    return video

def is_video_transparent(video):
    """
    Checks if the first frame of the mask of the given 'video'
    has, at least, one transparent pixel.
    """
    # We need to detect the transparency from the mask
    video = VideoParser.to_moviepy(video, do_include_mask = True)

    # We need to find, by now, at least one transparent pixel
    # TODO: I would need to check all frames to be sure of this above
    return np.any(video.mask.get_frame(t = 0) == 1)