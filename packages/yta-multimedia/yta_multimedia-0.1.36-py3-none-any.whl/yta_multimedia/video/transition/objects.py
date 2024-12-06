"""
    These classes are to be used internally, the ones 
    that you can use in the project to build videos 
    are exposed in the __init__.py file.

    This is one example of use of the alpha transition:

    youtube_url = 'https://www.youtube.com/watch?v=mylQ5Q9GRgs&pp=ygUQYWxwaGEgdHJhbnNpdGlvbg%3D%3D'
    alpha_video = YoutubeVideo(youtube_url).download(output_filename = create_temp_filename('youtube_alpha.mp4'))
    alpha_video = VideoParser.to_moviepy(alpha_video)
    video = VideoParser.to_moviepy('prueba.mp4', False, True).with_subclip(0, 2)
    video2 = VideoParser.to_moviepy('caminando_bosque_60fps.mp4', False, True).with_subclip(0, 2)
    transition = VideoTransition(TransitionMode.PLAYING, duration = 1, method = TransitionMethod.alpha, alpha_video = alpha_video)
    concatenated = TransitionGenerator.apply([video, video2], [transition])
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWith, MoviepyArgument
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.frames.numpy_frame_helper import FrameMaskingMethod
from yta_multimedia.video.edition.effect.moviepy.alpha import MoviepyAlphaTransitionHandler
from yta_multimedia.video.edition.duration import set_video_duration, ExtendVideoMode, EnshortVideoMode
from yta_multimedia.video.position import Position
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.programming.error_message import ErrorMessage
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy import ImageClip, CompositeVideoClip, VideoClip, concatenate_videoclips
from typing import Callable

import numpy as np


class TransitionMode(Enum):
    """
    Class to represent the transition modes (the way we
    join the videos between a transition).
    """
    FREEZE = 'freeze'
    """
    Freeze the last frame of the first video and the first
    frame ot he second video and make the transition with
    those static frames so the duration is extended by the
    transition duration.
    """
    PLAYING = 'playing'
    """
    Keep both video playing while the transition is run.
    """

class VideoTransition:
    """
    Class to encapsulate the logic to apply in a video 
    transition, containing the mode of transition and 
    the logic to apply on it.
    """
    mode: TransitionMode
    """
    The mode of transition we want to apply.
    """
    duration: float
    """
    The duration that the transition logic will last being
    applied.
    """
    method: Callable
    """
    The method we want to apply as the transition logic, that
    must be a static function of the Transition class.
    """
    kwargs: list
    """
    Other attributes we could need for some specific type of
    transition generation methods.
    """
    def __init__(self, mode: TransitionMode, duration: float, method: Callable, **kwargs):
        """
        The provided 'method' must be one of the static methods
        existing in the Transition class.
        """
        if not PythonValidator.is_class_staticmethod(TransitionMethod, method):
            raise Exception('The provided "method" parameter is not an static method of the Transition class.')
        
        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))
        # TODO: Maybe make 'duration' be multiple of frame_time
        # and multiple of a pair frame_time to allow the 
        # transition work equally in both videos

        mode = TransitionMode.to_enum(mode)
        
        self.mode = mode
        self.duration = duration
        self.method = method
        self.kwargs = kwargs

class Transition:
    """
    Class to encapsulate all the transition methods we
    handle in our system. Each transition is a way of
    connecting two different videos.

    This class is built to be used within the
    TransitionGenerator class as parameter to build 
    videos with those transitions.
    """
    video1: VideoClip = None
    """
    The video that comes before the transition.
    """
    transition: VideoTransition = None
    """
    The transition to apply between video1 and video2.
    """
    video2: VideoClip = None
    """
    The video that comes after the transition.
    """
    _final_video: VideoClip = None
    """
    The final video that contains the video1 and video2
    mixed with the transition in the middle. If this
    attribute is set it means that the transition has 
    been applied.
    """
    # TODO: I need to check if I should save the videos
    # and transition clip separately or just the 
    # concatenated one

    @property
    def is_ready(self):
        """
        Return True if the final video has been built by applying
        the desired transition and can be extracted from 'output'
        attribute.
        """
        return self._final_video is not None
    
    @property
    def output(self):
        """
        The output video result of combining the videos and the
        transition in the middle. This will be None if the transition
        has not been applied yet.
        """
        return self._final_video

    def __init__(self, video1: VideoClip, transition: VideoTransition, video2: VideoClip):
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        
        if not PythonValidator.is_instance(transition, VideoTransition):
            raise Exception('The provided "transition" is not a VideoTransition instance.')
        
        self.video1 = video1
        self.transition = transition
        self.video2 = video2

    def build(self):
        """
        Build the final video that includes the two videos provided
        with the transition in the middle. This method will build it
        if it is not ready, or return it if it has been built 
        previously.

        The result is a single video that you could use for the next
        transition if needed.
        """
        if not self.is_ready:
            video1, transition, video2 = Transition.create_transition(self.video1, self.video2, self.transition)
            self._final_video = concatenate_videoclips([video1, transition, video2])

        return self.output

    @staticmethod
    def create_transition(video1, video2, transition: VideoTransition = None):
        """
        Create the transition between 'video1' and 'video2' and 
        return the items in the next order: video1, transition,
        video2. Those items are ready to be concatenated in 
        that order to obtain both videos played with the expected
        transition in between.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        
        if not PythonValidator.is_instance(transition, VideoTransition):
            raise Exception('The provided "transition" is not a VideoTransition instance.')

        # Handle transition and videos
        if transition.mode == TransitionMode.FREEZE:
            # Original videos are not modified
            transition_first_clip = ImageClip(VideoFrameExtractor.get_last_frame(video1), duration = transition.duration).with_fps(60)
            transition_second_clip = ImageClip(VideoFrameExtractor.get_first_frame(video2), duration = transition.duration).with_fps(60)
        elif transition.mode == TransitionMode.PLAYING:
            if transition.duration > video1.duration or transition.duration > video2.duration:
                # TODO: Make this Exception more description (which video is wrong)
                # and talk about that we use the half of the provided duration
                raise Exception(f'The provided "transition.duration" parameter {str(transition.duration)} is not valid according to the provided video duration.')
            
            transition_first_clip = video1.with_subclip(video1.duration - transition.duration, video1.duration)
            transition_second_clip = video2.with_subclip(0, transition.duration)
            video1 = video1.with_subclip(0, video1.duration - transition.duration)
            video2 = video2.with_subclip(transition.duration, video2.duration)
        
        return video1, transition.method(video1 = transition_first_clip, video2 = transition_second_clip, **transition.kwargs), video2
    
class TransitionMethod:
    """
    This class is for internal use only. It is used by
    the TransitionGenerator class to generate clip
    transitions.

    This class encapsulates the functionality to generate 
    transition clips and the different methods to build
    them.
    """
    @staticmethod
    def slide(video1: VideoClip, video2: VideoClip, side: Position = Position.OUT_LEFT, **kwargs):
        """
        Simple transition in which the last frame of the provided 'video1'
        is replaced by the first frame of the provided 'video2' by sliding
        from right to left.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        side = Position.to_enum(side)

        # TODO: Sorry, I need to make sure these 2 videos
        # are 1920x1080 sized to be able to manage the
        # transition. I should use 'resize_video' here 
        # below to force it (?)

        # We accept the animation from this 4 positions
        ACCEPTED_POSITIONS = [Position.OUT_LEFT, Position.OUT_RIGHT, Position.OUT_TOP, Position.OUT_BOTTOM]
        if side not in ACCEPTED_POSITIONS:
            accepted_positions_str = ', '.join([pos.name for pos in ACCEPTED_POSITIONS])
            raise Exception(f'The provided "side" parameter "{str(side.name)}" is not a valid position for the slide animation. The valid options are: {accepted_positions_str}')

        # We calculate the end position based on provided 'side'
        pos = side.get_moviepy_center_tuple()
        t1_end_position = (pos[0], pos[1])
        if side == Position.OUT_TOP:
            t2_start_position = (0, video1.h)
        elif side == Position.OUT_BOTTOM:
            t2_start_position = (0, -video2.h)
        elif side == Position.OUT_RIGHT:
            t2_start_position = (-video2.w, 0)
        elif side == Position.OUT_LEFT:
            t2_start_position = (video1.w, 0)

        # Transition from last frame of video1 to first of video2
        t1_arg = MoviepyArgument((0, 0), t1_end_position, TFunctionSetPosition.linear, RateFunction.linear)
        transition_clip_1 = MoviepyWith.apply(video1, with_position = t1_arg)

        t1_position = transition_clip_1.pos(t = 0)
        t2_arg = MoviepyArgument(t2_start_position, (t1_position[0], t1_position[1]), TFunctionSetPosition.linear, RateFunction.linear)
        transition_clip_2 = MoviepyWith.apply(video2, with_position = t2_arg)

        return CompositeVideoClip([
            transition_clip_1,
            transition_clip_2
        ])
    
    @staticmethod
    def alpha(video1: VideoClip, video2: VideoClip, alpha_video: VideoClip, alpha_processing_method: FrameMaskingMethod = FrameMaskingMethod.MEAN, **kwargs):
        """
        Transition that involves an alpha clip in between the
        two provided 'video1' and 'video2' clips by applying
        that alpha clip as a mask in the second one to appear
        over the first one.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        alpha_video = VideoParser.to_moviepy(alpha_video)
        alpha_processing_method = FrameMaskingMethod.to_enum(alpha_processing_method)

        # We need to adjust the clip to the transition duration
        if (alpha_video.duration != video1.duration):
            alpha_video = set_video_duration(alpha_video, video1.duration, ExtendVideoMode.SLOW_DOWN, EnshortVideoMode.SPEED_UP)

        # TODO: Can we avoid MoviepyAlphaTransitionHandler and use
        # generic classes and .to_mask()' (?)
        mask_clip = MoviepyAlphaTransitionHandler.alpha_clip_to_mask_clip(alpha_video, masking_method = alpha_processing_method)
        video2 = video2.with_mask(mask_clip)

        return CompositeVideoClip([
            video1,
            video2
        ])

class TransitionHandler:
    """
    Class to simplify and encapsulate the functionality
    related to transition between videos. This class has
    been built to simplify the way we apply transitions.
    """
    
    # TODO: Check this below to understand a problem
    """
        There is a big problem here. Even if you put
        the same instance in two different transitions,
        that doesn't mean that you want the second one
        to be updated. You could want them to be different
        transitions using the same video as it is. If you
        want to use the result of a previous Transition you
        should do it by applying the '.build()' result of
        the first one as the input for the next one, and
        you cannot set it that easy

        There is an example below:

        Transition(
            Transition(
                'video',
                VideoTransition(),
                'video2'
            ),
            VideoTransition(),
            'video2'
        )
    """
    @staticmethod
    def apply(videos, transitions: list[VideoTransition] = None):
        """
        Applies the provided 'transitions' between the also provided
        'videos'. The amount of 'transitions' provided must be one 
        less than the 'videos' provided.

        This method will use the final video of each transition as 
        the first video of the next transition as it is placing the
        provided 'transitions' in between all provided 'videos'.

        So, the sequence is the next.
        1. The 'videoX' is played completely.
        2. The transition is played completely.
        3. Go to step 1 with the next video until last one
        4. Last video is played completely
        """
        if not PythonValidator.is_list(videos):
            videos = [VideoParser.to_moviepy(video)]
        
        if len(videos) == 1:
            return videos[0]

        if not PythonValidator.is_list(transitions):
            if not PythonValidator.is_instance(transitions, VideoTransition):
                raise Exception('The provided "transitions" parameter is not a list of VideoTransition nor a single VideoTransition.')
            else:
                transitions = [transitions] * (len(videos) - 1)
        else:
            if len(transitions) != len(videos) - 1:
                raise Exception(f'The number of videos is {str(len(videos))} and the amount of transitions must be {str(len(videos) - 1)} and you provided {str(len(transitions))} transitions.')

        videos = [VideoParser.to_moviepy(video) for video in videos]

        # TODO: Apply the new 'Transition'
        video_transitions = []
        for i in range(1, len(videos)):
            video, video_transition, next_video = Transition.create_transition(videos[i - 1], videos[i], transitions[i - 1])

            videos[i - 1] = video
            videos[i] = next_video
            video_transitions.append(video_transition)
            
        clips_to_concat = []
        for video, video_transition in zip(videos[:-1], video_transitions):
            clips_to_concat.extend([video, video_transition])
        clips_to_concat.append(videos[-1])

        return concatenate_videoclips(clips_to_concat)


def get_alpha_clip_core_part(alpha_video: VideoClip):
    """
    Process the 'alpha_video' and subclip it to the
    core part only. This part is the one in which
    the animation/effect/transition is happening,
    removing empty frames at the begining or the end
    of the video.

    This method iterates over the frames to detect
    the ones that are not similar to the previous
    ones at the begining and at the end of the 
    provided 'alpha_video'.

    TODO: This method can be updated, it is very
    experimental.
    """
    alpha_video = VideoParser.to_moviepy(alpha_video)

    alpha_frames = list(alpha_video.iter_frames())
    last_frame_index = int(alpha_video.duration * alpha_video.fps) - 1

    previous_frame = None
    first_index = 0
    last_index = last_frame_index

    # Look for non-core part at the begining
    for index, frame in enumerate(alpha_frames):
        if previous_frame is None:
            previous_frame = frame
        else:
            # This calculates the difference
            #print(np.sum(np.abs(frame - previous_frame)))
            if not np.array_equal(frame, previous_frame):
                first_index = index
                break
            else:
                previous_frame = frame

    previous_frame = None
    
    # Look for non-core part at the end
    for index, frame in enumerate(reversed(alpha_frames)):
        if previous_frame is None:
            previous_frame = frame
        else:
            # This calculates the difference
            #print(np.sum(np.abs(frame - previous_frame)))
            if not np.array_equal(frame, previous_frame):
                last_index = last_frame_index - index
                break
            else:
                previous_frame = frame

    alpha_video = alpha_video.with_subclip(first_index * (1 / alpha_video.fps), last_index * (1 / alpha_video.fps))

    # alpha_frames = alpha_frames[first_index:last_index + 1]
    # alpha_video = VideoClip(lambda t: alpha_frames[int(t * alpha_video.fps)], duration = len(alpha_frames) * (1 / alpha_video.fps)).with_fps(alpha_video.fps)

    return alpha_video