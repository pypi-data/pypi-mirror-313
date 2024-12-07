from yta_multimedia.video.parser import VideoParser
from yta_general_utils.image.converter import ImageConverter
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from moviepy import VideoClip
from imageio import imsave
from typing import Union

import numpy as np


class FrameExtractionType(Enum):
    """
    Enum to simplify the way we indicate the frame extraction
    operation we want to execute.
    """
    TIME = 'time'
    FRAME_NUMBER = 'frame_number'

class VideoFrameExtractor:
    """
    Class to simplify the process of extracting video frames by time
    or frame number.

    A moviepy clip is built by consecutive frames. The first frame is
    on t = 0, and the next frames are obtained by applying a (a, b]
    interval. This means that if we a have a video of 10 fps, each 
    frame will last 0.1s. So, considering the previous condition, the
    second frame will be at 0.1s, so you will be able to access it by
    providing a time between (0.000000000001, 0.1].
    """
    # # TODO: Implement the 'output_filename' optional parameter to store
    # # the frames if parameter is provided.
    # @classmethod
    # def _get_frame_time(cls, video, frame_number_or_time, extraction_type: FrameExtractionType):
    #     """
    #     Returns the time to obtain the frame of the provided 'video'
    #     according to the provided 'frame_number_or_time' parameter and
    #     the desired 'extraction_type'.

    #     This method is useful to be used first to validate that the
    #     frame times or numbers are valid and avoid getting all the 
    #     frames and loading them in memory if it is going to fail.
    #     """
    #     video = VideoParser.to_moviepy(video)
    #     extraction_type = FrameExtractionType.to_enum(extraction_type)
        
    #     if not NumberValidator.is_positive_number(frame_number_or_time):
    #         raise Exception('The provided "frame_number_or_time" is not a valid number.')
        
    #     if extraction_type == FrameExtractionType.FRAME_NUMBER:
    #         max_frame_number = video.fps * video.duration
    #         if frame_number_or_time > max_frame_number:
    #             raise Exception(f'The provided "frame_number" parameter {str(frame_number_or_time)}" is not valid. The maximum is {str(max_frame_number)}.')
            
    #         frame_number_or_time = frame_number_or_time * 1.0 / video.fps
    #     elif extraction_type == FrameExtractionType.TIME:
    #         if frame_number_or_time > video.duration:
    #             raise Exception(f'The provided "time" parameter {str(frame_number_or_time)} is not valid. The maximum is {str(video.duration)}.')
            
    #     return frame_number_or_time

    # # TODO: I think I won't use this because I need to validate them first
    # @classmethod
    # def _get_frame(cls, video, frame_number_or_time, extraction_type: FrameExtractionType, output_filename: str = None):
    #     """
    #     Returns the frame of the provided 'video' according to the provided
    #     'frame_number_or_time' parameter and the desired 'extraction_type'.
    #     """
    #     video = VideoParser.to_moviepy(video)

    #     frame = video.get_frame(t = cls._get_frame_time(video, frame_number_or_time, extraction_type))

    #     if output_filename:
    #         cls._save_frame(frame, output_filename)

    #     return frame
    
    # @classmethod
    # def _get_frames(cls, video, frame_numbers_or_times, extraction_type: FrameExtractionType):
    #     """
    #     This method validates if all the provided 'frame_numbers_or_times'
    #     array parameter items are valid or not and them get all the frames
    #     and returns them as an array. This is optimum as it doesn't load
    #     frames until it's been verified the condition that all are valid.
    #     """
    #     video = VideoParser.to_moviepy(video)

    #     # Validate and get all times to obtain the frames later
    #     times = [cls._get_frame_time(video, frame_number_or_time, extraction_type) for frame_number_or_time in frame_numbers_or_times]

    #     return [video.get_frame(t = time) for time in times]
    
    # @classmethod
    # def get_frames_by_time(cls, video, times: list[float]):
    #     """
    #     Returns the frames (as numpy arrays) from the provided 'video'
    #     that corresponds to the provided 'times' time momnets of the
    #     video.

    #     This method will raise an Exception if the limits are not valid
    #     for the given 'video'.
    #     """
    #     return cls._get_frames(video, times, FrameExtractionType.TIME)

    # @classmethod
    # def _save_frame(cls, frame, output_filename: str):
    #     if not output_filename:
    #         return None
        
    #     # TODO: Validate 'output_filename'
        
    #     # TODO: This is how 'video.save_frame' works
    #     # https://github.com/Zulko/moviepy/blob/master/moviepy/video/VideoClip.py#L166
    #     # from imageio import imsave
    #     # im = self.get_frame(t)
    #     # if with_mask and self.mask is not None:
    #     #     mask = 255 * self.mask.get_frame(t)
    #     #     im = np.dstack([im, mask]).astype("uint8")
    #     # else:
    #     #     im = im.astype("uint8")

    #     imsave(output_filename, frame.astype("uint8"))

    #     return True

    # @classmethod
    # def get_frame_by_time(cls, video, time: float, output_filename: str = None):
    #     """
    #     Returns the frame (as numpy arrays) from the provided 'video'
    #     that corresponds to the provided 'time' moment.

    #     This method will raise an Exception if the limits are not valid
    #     for the given 'video'.
    #     """
    #     frame = cls.get_frames_by_time(video, [time])[0]

    #     if output_filename:
    #         cls._save_frame(frame, output_filename)

    #     return frame
    
    # @classmethod
    # def get_frames_by_time_from_start_to_end(cls, video, start_time: float, end_time: float):
    #     """
    #     Returns the frames (as numpy arrays) from the provided 'video'
    #     that corresponds to the lapse of time between the provided
    #     'start_time' and 'end_time'.

    #     This method will raise an Exception if the limits are not valid
    #     for the given 'video'.
    #     """
    #     video = VideoParser.to_moviepy(video)

    #     # Validate start and end parameters
    #     if not NumberValidator.is_positive_number(start_time) or start_time < 0 or start_time > video.duration:
    #         raise Exception(f'The provided "start_time" parameter "{str(start_time)}" is not valid. It must be a positive number between 0 and the video duration ({str(video.duration)}).')
    #     if not NumberValidator.is_positive_number(end_time) or end_time < 0 or end_time < start_time or end_time > video.duration:
    #         raise Exception(f'The provided "end_time" parameter "{str(end_time)}" is not valid. It must be a positive number between 0 and the video duration ({str(video.duration)}), and greater than the provided "start_time" parameter.')
        
    #     total_frames = int(video.duration * video.fps)
    #     time_moments = []
    #     for frame in range(total_frames):
    #         frame_time_moment = frame / video.fps  # tiempo en segundos para el frame actual
    #         if start_time <= frame_time_moment <= end_time:
    #             time_moments.append(frame_time_moment)

    #     return cls.get_frames_by_time(video, time_moments)

    # @classmethod
    # def get_frame_by_frame_number(cls, video, frame_number: int, output_filename: str = None):
    #     """
    #     Returns the frame (as numpy array) for the provided 'video' that
    #     corresponds to the provided 'frame_number'.

    #     This method will raise an Exception if the provided 'frame_number'
    #     is not a valid frame number for the given 'video'.
    #     """
    #     frame = cls._get_frame(video, frame_number, FrameExtractionType.FRAME_NUMBER)

    #     if output_filename:
    #         cls._save_frame(frame, output_filename)

    #     return frame
    
    # @classmethod
    # def get_frames_by_frame_number(cls, video, frame_numbers: list[int]):
    #     """
    #     Returns the frames (as numpy arrays) from the provided 'video'
    #     that corresponds to the provided 'frame_numbers'.

    #     This method will raise an Exception if the limits are not valid
    #     for the given 'video'.
    #     """
    #     return cls._get_frames(video, frame_numbers, FrameExtractionType.FRAME_NUMBER)
    
    # @classmethod
    # def get_frames_by_frame_number_from_start_to_end(cls, video, start_frame: float, end_frame: float):
    #     """
    #     Returns the frames (as numpy arrays) from the provided 'video' 
    #     from the 'start_frame' to the 'end_frame'.

    #     This method will raise an Exception if the limits are not valid
    #     for the given 'video'.
    #     """
    #     video = VideoParser.to_moviepy(video)

    #     max_frame_number = int(video.fps * video.duration)
    #     # Validate start and end parameters
    #     if not NumberValidator.is_positive_number(start_frame) or start_frame < 0 or start_frame > max_frame_number:
    #         raise Exception(f'The provided "start_frame" parameter "{str(start_frame)}" is not valid. It must be a positive number between 0 and the maximum frame ({str(max_frame_number)}).')
    #     if not NumberValidator.is_positive_number(end_frame) or end_frame < 0 or end_frame < start_frame or end_frame > max_frame_number:
    #         raise Exception(f'The provided "end_frame" parameter "{str(end_frame)}" is not valid. It must be a positive number between 0 and the maximum frame ({str(max_frame_number)}), and greater than the provided "start_time" parameter.')
        
    #     frames = [frame for frame in range(start_frame, end_frame + 1)]
    #     time_moments = [cls._get_frame_time(video, frame, FrameExtractionType.FRAME_NUMBER) for frame in frames]

    #     return cls.get_frames_by_time(video, time_moments)

    @staticmethod
    def get_frame_by_number(video: VideoClip, t: int = 0, output_filename: Union[str, None] = None):
        """
        Get the frame 't' of the provided 'video'. The frame number
        must be a valid one.
        """
        frame = VideoFrameExtractor.get_frames_by_number(video, [t])

        if output_filename:
            # TODO: Why type (?)
            #imsave(output_filename, frame.astype("uint8"))
            imsave(output_filename, frame)

        return frame

    @staticmethod
    def get_frames_by_number(video, t: list[int] = [0]):
        """
        Get all the 't' frames of the provide d'video'. Those frame
        numbers must be valid.
        """
        if not PythonValidator.is_list(t):
            if NumberValidator.is_positive_number(t):
                t = [t]
            else:
                raise Exception('The provided "t" is not an array of frame numbers nor a single one.')
            
        return [VideoFrameExtractor.get_frame(video, FrameExtractionType.FRAME_NUMBER, t_) for t_ in t]
    
    @staticmethod
    def get_frame_by_time(video: VideoClip, t: float = 0.0, output_filename: Union[str, None] = None):
        """
        Get the frame in the provided 't' time moment of the
        provided 'video'. The frame time must be a valid one,
        between 0 and the video duration.
        """
        frame = VideoFrameExtractor.get_frames_by_time(video, [t])[0]

        if output_filename:
            # TODO: Why type (?)
            #imsave(output_filename, frame.astype("uint8"))
            imsave(output_filename, frame)

        return frame

    @staticmethod
    def get_frames_by_time(video, t: list[float] = [0.0]):
        """
        Get all the frame corresponding to the time moments in
        provided 't' of the provided 'video'. All frame times
        must be valid, between 0 and the video duration.
        """
        if not PythonValidator.is_list(t):
            if NumberValidator.is_positive_number(t):
                t = [t]
            else:
                raise Exception('The provided "t" is not an array of frame times nor a single one.')
            
        return [VideoFrameExtractor.get_frame(video, FrameExtractionType.TIME, t_) for t_ in t]
    
    @staticmethod
    def get_frame(video, mode: FrameExtractionType = FrameExtractionType.FRAME_NUMBER, t: Union[float, int] = 0):
        """
        Get the frame corresponding to the provided 't' frame number
        or time moment. Feel free to use the moviepy .get_frame()
        method instead.

        This is my own method due to some problems with the original
        moviepy .get_frame() and because of its laxity.
        """
        video = VideoParser.to_moviepy(video)
        mode = FrameExtractionType.to_enum(mode)

        if not NumberValidator.is_positive_number(t):
            raise Exception('The provided "t" value is not a positive number.')

        if mode == FrameExtractionType.FRAME_NUMBER:
            t = int(t)
        elif mode == FrameExtractionType.TIME:
            t = float(t)

        frames = VideoFrameExtractor.get_all_frames(video)
        duration = video.duration
        fps = video.fps

        if mode == FrameExtractionType.FRAME_NUMBER and t > len(frames):
            raise Exception(f'The provided "t" frame number "{str(t)}" is not valid.. The maximum is {str(len(frames - 1))}.')
        elif mode == FrameExtractionType.TIME and t > duration:
            raise Exception(f'The provided "t" frame duration "{str(t)}" is not valid. The maximum is {str(duration)}.')

        if mode == FrameExtractionType.FRAME_NUMBER:
            frame = frames[t]
        elif mode == FrameExtractionType.TIME:
            if t == duration:
                frame = frames[-1]
            else:
                frames_number = int(fps * duration)
                frame_duration = duration / frames_number
                # We add a 10% of frame_duration to make sure it fits
                # the expected frame
                frame = frames[int(t * fps + frame_duration * 0.1)]

        return frame

    @classmethod
    def get_all_frames(cls, video):
        """
        Returns all the frames from the provided 'video'.
        """
        video = VideoParser.to_moviepy(video)

        return [frame for frame in video.iter_frames()]
    
    @staticmethod
    def get_first_frame(video):
        """
        Obtain the first frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        return VideoFrameExtractor.get_all_frames(video)[0]
    
    @staticmethod
    def get_last_frame(video):
        """
        Obtain the last frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        return VideoFrameExtractor.get_all_frames(video)[-1]
    
    # TODO: Would be perfect to have some methods to turn frames into
    # RGBA denormalized (0, 255) or normalized (0, 1) easier because
    # it is needed to work with images and other libraries. Those 
    # methods would iterate over the values and notice if they are in
    # an specific range so they need to be change or even if they are
    # invalid values (not even in [0, 255] range because they are not
    # rgb or rgba colors but math calculations).
    # This is actually being done by the VideoMaskHandler
    @classmethod
    def get_frame_as_rgba_by_time(cls, video, time: int, do_normalize: bool = False, output_filename: str = None):
        """
        Gets the frame of the requested 'time' of the provided
        'video' as a normalized RGBA numpy array that is built
        by joining the rgb frame (from main clip) and the alpha
        (from .mask clip), useful to detect transparent regions.
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)

        # We first normalize the clips
        main_frame = cls.get_frame_by_time(video, time) / 255  # RGB numpy array normalized 3d <= r,g,b
        mask_frame = cls.get_frame_by_time(video.mask, time)[:, :, np.newaxis]  # Alpha numpy array normalized 1d <= alpha
        # Combine RGB of frame and A from mask to RGBA numpy array (it is normalized)
        frame_rgba = np.concatenate((main_frame, mask_frame), axis = 2) # 4d <= r,g,b,alpha

        if output_filename:
            # TODO: Check extension
            ImageConverter.numpy_image_to_pil(frame_rgba).save(output_filename)
            # TODO: Write numpy as file image
            # Video mask is written as 0 or 1 (1 is transparent)
            # but main frame is written as 0 to 255, and the
            # 'numpy_image_to_pil' is expecting from 0 to 1
            # (normalized) instead of from 0 to 255 so it won't
            # work

        if not do_normalize:
            frame_rgba *= 255

        return frame_rgba
    