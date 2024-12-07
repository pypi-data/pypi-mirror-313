from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_multimedia.video.edition.duration import set_video_duration
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.programming.parameter_validator import PythonValidator
from typing import Union
from moviepy import VideoClip, CompositeVideoClip, concatenate_videoclips
from moviepy.Clip import Clip
from copy import copy

import numpy as np


class VideoHandler:
    """
    Class created to simplify and encapsulate some basic
    calculations related to a video, its frames and more
    properties.
    """
    video: Clip = None
    """
    The video to handle.
    """
    _frame_duration: float = None
    _frame_time_moments: list = None

    def __init__(self, video: Clip):
        video = VideoParser.to_moviepy(video)

        self.video = video

    @property
    def frame_duration(self):
        """
        The frame duration of the video, calculated with this
        formula:

        frame_duration = duration / (duration * fps)
        """
        if self._frame_duration is None:
            self._frame_duration = 1 / self.video.fps

        return self._frame_duration
    
    @property
    def frame_time_moments(self):
        """
        The list of frame time moments (ts) to build the clip
        frame by frame. This can be used to precalculate video
        positions, resizes or rotations, in order to apply them
        later one by one, frame by frame, reading directly form
        an array.

        You can access to an specific time moment by using the
        'get_frame_time_moment' method.
        """
        if self._frame_time_moments is None:
            self._frame_time_moments = np.linspace(0, self.video.duration, self.frames_number)

        return self._frame_time_moments
    
    @property
    def frames_number(self):
        return self.video.n_frames
    
    def get_frame_number_by_time_moment(self, t: float):
        """
        Return the frame number (from 0 to the last one)
        according to the frame time moment 't' provided.

        The frame number is calculated with the next formula:

        rotations[int((t + frame_duration * 0.1) // frame_duration)]

        The '+ frame_duration * 0.1' part is needed to make sure
        each frame access is different (due to floating points
        errors)
        """
        if not NumberValidator.is_positive_number(t):
            raise Exception(f'The provided "t" parameter "{str(t)}" is not a valid frame time moment.')
        
        return VideoHandler.t_to_frame_index(t, self.frame_duration)
        # TODO: What about looking for in in the array (?)
        # Maybe I don't find it because of floating points (?)

    # TODO: Maybe move this method to a VideoMaskInverter
    # class...
    def invert(self):
        """
        Invert the received 'video' (that must be a moviepy 
        mask or normal clip) and return it inverted as a
        VideoClip. If the provided 'video' is a mask, this 
        will be also a mask.

        If the 'clip' provided is a mask clip, remember to
        set it as the new mask of your main clip.

        This inversion is a process in which the numpy array
        values of each frame are inverted by substracting the
        highest value. If the frame is an RGB frame with 
        values between 0 and 255, it will be inverted by 
        doing 255 - X on each frame pixel value. If it is
        normalized and values are between 0 and 1 (it is a 
        mask clip frame), by doing 1 - X on each mask frame
        pixel value.
        """
        mask_frames = [VideoFrame(frame).inverted() for frame in self.video.iter_frames()]

        # TODO: Which calculation is better, t * fps or t // frame_duration (?)
        # TODO: What if we have fps like 29,97 (?) I proposed forcing
        # the videos to be 60fps always so we avoid this problem
        return VideoClip(lambda t: mask_frames[int(t * self.video.fps)], is_mask = self.video.is_mask).with_fps(self.video.fps)
    
    def prepare_background_clip(self, background_video: Union[str, Clip]):
        """
        Prepares the provided 'background_video' by modifying its duration to
        be the same as the provided 'video'. By default, the strategy is 
        looping the 'background_video' if the 'video' duration is longer, or
        cropping it if it is shorter. This method returns the background_clip
        modified according to the provided 'video'.

        This method will raise an Exception if the provided 'video' or the provided
        'background_video' are not valid videos.

        TODO: Add a parameter to be able to customize the extend or enshort
        background strategy.
        """
        background_video = VideoParser.to_moviepy(background_video)

        background_video = set_video_duration(background_video, self.video.duration)

        return background_video

    @staticmethod
    def t_to_frame_index(t: float, frame_duration: float):
        """
        Transform the provided 't', applying the also provided
        'frame_duration' to the frame times array index to be
        able to access to its value.

        This method applies the next formula:

        int((t + frame_duration * 0.1) // frame_duration)
        """
        # This is apparently the same as int(t * self.video.fps)
        return int(t // frame_duration)
        return int((t + frame_duration * 0.1) // frame_duration)

    @staticmethod
    def concatenate_videos(videos: list[Clip]):
        """
        Concatenate the provided 'videos' but fixing the
        videos dimensions. It will wrap any video that
        doesn't fit the 1920x1080 scene size with a full
        transparent background to fit those dimensions.
        """
        if not PythonValidator.is_list(videos):
            videos = [videos]

        videos = [VideoParser.to_moviepy(video) for video in videos]
        videos = [VideoHandler(video).wrap_with_transparent_background() for video in videos]
        
        return concatenate_videoclips(videos)
    
    def wrap_with_transparent_background(self):
        """
        Put a full transparent background behind the video
        if its size is not our default scene (1920x1080) and
        places the video on the center of this background.

        This method works with a copy of the original video so
        only the returned one is changed.
        """
        # TODO: This should be a constant
        MOVIEPY_DEFAULT_SCENE_SIZE = (1920, 1080)

        video = copy(self.video)
        # TODO: Is this changing the variable value or do I
        # need to do by position (?)
        if self.video.size != MOVIEPY_DEFAULT_SCENE_SIZE:
            # I place the video at the center of the new background but
            # I reposition it to place with its center in the same place
            # as the original one
            original_center_positions = []
            # TODO: Careful with this t
            for t in self.frame_time_moments:
                pos = video.pos(t)
                original_center_positions.append((pos[0], pos[1]))

            video = CompositeVideoClip([
                ClipGenerator.get_default_background_video(duration = video.duration),
                video.with_position(('center', 'center'))
            ]).with_position(lambda t: (
                original_center_positions[VideoHandler.t_to_frame_index(t, 1 / video.fps)][0] - MOVIEPY_DEFAULT_SCENE_SIZE[0] / 2,
                original_center_positions[VideoHandler.t_to_frame_index(t, 1 / video.fps)][1] - MOVIEPY_DEFAULT_SCENE_SIZE[1] / 2
            ))

        return video