from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.enums import FileType
from yta_general_utils.file.filename import filename_is_type
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoFileClip
from moviepy.Clip import Clip
from typing import Union


class VideoParser:
    """
    Class to simplify the way we parse video parameters.
    """
    @classmethod
    def to_moviepy(cls, video: Union[str, Clip], do_include_mask: bool = False):
        """
        This method is a helper to turn the provided 'video' to a moviepy
        video type. If it is any of the moviepy video types specified in
        method declaration, it will be returned like that. If not, it will
        be load as a VideoFileClip if possible, or will raise an Exception
        if not.

        The 'do_include_mask' parameter includes the mask in the video if
        True value provided. The 'do_check_duration' parameter checks and
        updates the real video duration to fix a bug in moviepy lib.
        """
        if not video:
            raise Exception('No "video" provided.')
        
        # TODO: Maybe check if subclass of VideoClip
        if not PythonValidator.is_string(video) and not PythonValidator.is_instance(video, [Clip]):
            raise Exception('The "video" parameter provided is not a valid type. Check valid types in method declaration.')
        
        if PythonValidator.is_string(video):
            if not filename_is_type(video, FileType.VIDEO):
                raise Exception('The "video" parameter provided is not a valid video filename.')
            
            if not FileValidator.file_is_video_file(video):
                raise Exception('The "video" parameter is not a valid video file.')
            
            video = VideoFileClip(video, has_mask = do_include_mask)

        # TODO: This below just adds a mask attribute but
        # without fps and empty, so it doesn't make sense
        # if do_include_mask and not video.mask:
        #     video = video.add_mask()

        return video