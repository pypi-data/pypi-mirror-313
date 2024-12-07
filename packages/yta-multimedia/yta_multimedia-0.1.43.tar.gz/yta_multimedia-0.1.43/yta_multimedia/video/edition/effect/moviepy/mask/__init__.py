"""
    # TODO: I think we should move this file to 
    'yta_multimedia.video.frames' instead.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_general_utils.color import Color
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from moviepy import ColorClip, VideoClip
from typing import Union


class ClipGenerator:
    # TODO: Validate that this below is working because I've
    # never before used a transparent black background
    @staticmethod
    def get_default_background_video(size: tuple = (1920, 1080), duration: float = 1 / 60, is_transparent: bool = True):
        """
        Default full black background video that lasts
        'duration' seconds that represents our default moviepy
        scenario of 1920x1080 dimensions. This background is
        used for the basic position calculations. Check the
        transparent option if you are planning to stack some
        videos.

        The background can be build with a full transparent
        mask if 'is_transparent' provided as True.
        """
        opacity = 0.0 if is_transparent else 1.0

        return ClipGenerator.generate_color_background(size, [0, 0, 0], duration, 60, opacity)
    
    @staticmethod
    def generate_color_background(size: tuple, color: Union[Color, 'ColorString', str], duration: float = 1 / 60, fps: float = 60.0, opacity: float = 1.0):
        color = Color.parse(color)
        ClipValidator.validate_size(size)
        ClipValidator.validate_duration(duration)
        ClipValidator.validate_fps(fps)
        ClipValidator.validate_opacity(opacity)
        
        color_clip: ColorClip = ColorClip(size, color.as_rgb_array(), duration = duration).with_fps(fps)

        # A full opaque clip doesn't need a mask because it is,
        # by definition, full opaque
        if opacity < 1.0:
            color_clip = color_clip.with_mask(ClipMaskGenerator.get_uniform_mask(color_clip.size, color_clip.duration, color_clip.fps, opacity))

        return color_clip

# TODO: Move to another file, please, but avoid 
# cyclic import issues
class ClipValidator:
    """
    Class to simplify parameter validation while working
    with moviepy clips and clip parameters.
    """
    @staticmethod
    def validate_size(size: tuple):
        if not PythonValidator.is_tuple(size) or len(size) != 2 or not NumberValidator.is_number_between(size[0], 0, 5000) or not NumberValidator.is_number_between(size[1], 0, 5000):
            raise Exception('The provided "duration" is not a tuple or does not have the expected size (2) or the values are not between 0 and 5000.')
        
        return True
    
    @staticmethod
    def validate_duration(duration: float):
        # TODO: We could maybe accept 'fps' parameter to check
        # if 'duration' is a multiple
        if not NumberValidator.is_positive_number(duration, False):
            raise Exception('The provided "duration" is not a positive number.')
        
        return True
    
    @staticmethod
    def validate_fps(fps: int):
        if not NumberValidator.is_positive_number(fps):
            raise Exception('The provided "fps" is not a positive number.')
        
        return True
    
    @staticmethod
    def validate_opacity(opacity: float):
        if not NumberValidator.is_number_between(opacity, 0.0, 1.0):
            raise Exception('The provided "opacity" is not a float value between 1.0 and 0.0.')
        
        return True

# TODO: Move to another file, please, but avoid 
# cyclic import issues
class ClipMaskGenerator:
    @staticmethod
    def get_uniform_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60, opacity: float = 1.0):
        """
        Get a ColorClip of the 'opacity' provided, where 1.0 indicates
        full opaque and 0.0 full transparent, to be used as a mask. 
        
        This is called uniform because it uses a ColorClip that doesn't
        change along its duration time.
        """
        ClipValidator.validate_size(size)
        ClipValidator.validate_duration(duration)
        ClipValidator.validate_fps(fps)
        ClipValidator.validate_opacity(opacity)
        
        return ColorClip(size, opacity, is_mask = True, duration = duration).with_fps(fps)

    @staticmethod
    def get_uniform_opaque_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60):
        """
        Get a mask clip of the provided 'size' that is completely
        opaque and can be set as the mask of any other normal clip.
        
        This is called uniform because it uses a ColorClip that 
        doesn't change along its duration time.
        """
        return ClipMaskGenerator.get_uniform_mask(size, duration, fps, 1)
    
    @staticmethod
    def get_uniform_transparent_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60):
        """
        Get a maskclip  of the provided 'size' that is completely
        transparent and can be set as the mask of any other normal
        clip.

        This is called uniform because it uses a ColorClip that 
        doesn't change along its duration time.
        """
        return ClipMaskGenerator.get_uniform_mask(size, duration, fps, 0)
    
    @staticmethod
    def video_to_mask(video: VideoClip):
        """
        Turn the provided 'video' into a mask VideoClip that can be
        set as the mask of any other normal clip.
        """
        video = VideoParser.to_moviepy(video)

        # TODO: This is ok but very slow I think...
        mask_clip_frames = [VideoFrame(frame).as_mask() for frame in video.iter_frames()]

        return VideoClip(lambda t: mask_clip_frames[int(t * video.fps)], is_mask = True).with_fps(video.fps)

