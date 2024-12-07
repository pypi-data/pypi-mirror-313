from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.image.edition.filter.sketch import image_to_sketch, image_to_line_sketch
from yta_general_utils.image.converter import ImageConverter
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ImageSequenceClip
from typing import Union
from types import FunctionType


def video_to_sketch_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None]):
    # TODO: Document it
    return __video_to_frame_by_frame_filtered_video(video, image_to_sketch, output_filename)

def video_to_line_sketch_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None]):
    """
    This method is very very slow. I should try to optimize it or just
    use not, because it doesn't make sense as a video.
    """
    # TODO: Document it
    return __video_to_frame_by_frame_filtered_video(video, image_to_line_sketch, output_filename)

def __video_to_frame_by_frame_filtered_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], filter_func: FunctionType, output_filename: Union[str, None] = None):
    """
    Internal function to be used by any of our video editing methods
    that actually use image filter frame by frame. They do the same
    by only changing the filter we apply.
    """
    # TODO: Check if 'filter_func' is a function
    video = VideoParser.to_moviepy(video)

    original_frames = VideoFrameExtractor.get_all_frames(video)
    sketched_frames = []
    for original_frame in original_frames:
        sketched_frames.append(ImageConverter.pil_image_to_numpy(filter_func(original_frame)))

    sketched_video = ImageSequenceClip(sketched_frames, fps = video.fps).with_audio(video.audio)

    if output_filename:
        sketched_video.write_videofile(output_filename)

    return sketched_video

