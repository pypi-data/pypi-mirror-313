from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video import VideoHandler
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions import RateFunction
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip
from typing import Union


class MoviepyArgument:
    """
    Arguments used for 'with_position', 'resized' and 'rotated'
    simplified and unified to have the same structure to build
    new videos by modifying the basic moviepy effects.
    """
    def __init__(self, start: Union[int, tuple, float], end: Union[int, tuple, float], t_function: type, rate_func: RateFunction = RateFunction.linear):
        # TODO: 'start' and 'end' must be pure values which
        # means tuples if positions or numbers if resize or
        # rotate
        # TODO: Validate parameters
        self.start = start
        self.end = end
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: *args or **kwargs should be avoided as we must
        # define the 't_function' with the only parameters 
        # needed and make as much as we need. For example, we
        # should have '.arc_bottom' and '.arc_top' to avoid
        # passing a 'is_bottom' parameter because it would 
        # lost the common structure.

# TODO: Rename to MoviepyWithProcess or something more clear
# TODO: We need to accept a GraphicInterpolation as, at least,
# the 'with_position' parameter and build the needed values
# as it is happening for the example I leave in the 
# video\edition\effect\moviepy\position\move\refactor_this.py
# file code.
class MoviepyWith:
    """
    Class to encapsulate the 'resized', 'with_position' and
    'rotated' functionality and to be able to make one depend
    on the other by pre-calculating the values and then using
    them when positioning, resizing and rotating.

    You should use the same RateFunction if you are planning
    to move and resize the clip at the same time.
    """
    @staticmethod
    def apply(video: Clip, with_position: Union[MoviepyArgument, None] = None, resized: Union[MoviepyArgument, None] = None, rotated: Union[MoviepyArgument, None] = None):
        """
        Apply the property effects on the provided 'video'. This
        method will use a default background video to apply the
        effect.

        Default background is 1920x1080.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        return MoviepyWith.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration), with_position, resized, rotated)

    @staticmethod
    def apply_over_video(video: Clip, background_video: Clip, with_position: Union[MoviepyArgument, None] = None, resized: Union[MoviepyArgument, None] = None, rotated: Union[MoviepyArgument, None] = None):
        """
        Apply the property effects on the provided 'video'. This
        method will use the provided 'background_video' and 
        recalculate the position according to it.

        Background can be different to default scene of 1920x1080
        so positions will be adjusted to it.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)
        background_video = VideoParser.to_moviepy(background_video, True)

        # Prepare data for pre-calculations
        video_handler = VideoHandler(video)

        background_video = video_handler.prepare_background_clip(background_video)

        if resized:
            resizes = [resized.t_function(t, video.duration, resized.start, resized.end, resized.rate_func) for t in video_handler.frame_time_moments]
        else:
            # We build always this array because position calculation 
            # depends on it to be able to handle movement and resizing
            # at the same time
            resizes = [1 for _ in video_handler.frame_time_moments]

        positions = None
        if with_position:
            # TODO: Maybe this 'get_moviepy_position' can be replaced
            # with the Coordinate scene adapter method
            initial_position = get_moviepy_position(video, background_video, with_position.start)
            final_position = get_moviepy_position(video, background_video, with_position.end)
            positions = []
            for i, t in enumerate(video_handler.frame_time_moments):
                # Calculate each frame position based on each frame size
                initial_position = (initial_position[0] * resizes[i], initial_position[1] * resizes[i])
                final_position = (final_position[0] * resizes[i], final_position[1] * resizes[1])

                # TODO: This 'with_position.t_function' can have different
                # parameters to be able to work, so I don't know how to
                # dynamically handle this. For example, the 'at_position'
                # needs the video.size to be able to calculate where to
                # be centered...
                positions.append(with_position.t_function(t, video.duration, initial_position, final_position))
                
        rotations = None
        if rotated:
            rotations = [rotated.t_function(t, video.duration, rotated.start, rotated.end, rotated.rate_func) for t in video_handler.frame_time_moments]

        # TODO: Maybe avoid the 'resizes' with ones if is the
        # only one we will pass as param

        video = MoviepyWithPrecalculated.apply(video, positions, resizes, rotations)

        return CompositeVideoClip([
            background_video,
            video
        ])

        # I add frame_duration * 0.1 to make sure it fits the
        # next index
        video = video.resized(lambda t: resizes[int((t + frame_duration * 0.1) // frame_duration)])
        if positions:
            video = video.with_position(lambda t: positions[int((t + frame_duration * 0.1) // frame_duration)])
        if rotated:
            video = video.rotated(lambda t: rotations[int((t + frame_duration * 0.1) // frame_duration)])
        
        return video
    
class MoviepyWithPrecalculated:
    """
    Class to encapsulate the 'resized', 'with_position' and
    'rotated' functionality and to be able to make one depend
    on the other by the pre-calculated values provided and
    then using them when positioning, resizing and rotating.

    This class is just to apply the 'with_position', 'resized'
    and 'rotated' moviepy basic effects that must have been
    pre-calculated and passed as a list to be applied for each
    video frame.

    This class is useful when you want to pre-calculate your
    values by a custom function and not only a basic TFuntion
    available through the MoviepyWithArgument class.
    """
    @staticmethod
    def apply(video: Clip, with_position_list: Union[list, None] = None, resized_list: Union[list, None] = None, rotated_list: Union[list, None] = None):
        """
        Apply the property effects on the provided 'video'. This
        method will use the provided 'background_video' and 
        recalculate the position according to it.

        Background can be different to default scene of 1920x1080
        so positions will be adjusted to it.

        :param list with_position: The list of pre-calculated positions to apply.

        :param list resized: The list of pre-calculated resizes to apply.

        :param list rotated: The list of pre-calculated rotation effect to apply.
        """
        return MoviepyWithPrecalculated.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration), with_position_list, resized_list, rotated_list)

    @staticmethod
    def apply_over_video(video: Clip, background_video: Clip, with_position_list: Union[list, None] = None, resized_list: Union[list, None] = None, rotated_list: Union[list, None] = None):
        video = VideoParser.to_moviepy(video, do_include_mask = True)
        background_video = VideoParser.to_moviepy(background_video, True)
        
        # Prepare data for pre-calculations
        video_handler = VideoHandler(video)
        
        background_video = video_handler.prepare_background_clip(background_video)

        # Validate provided lists
        if resized_list is not None and len(resized_list) != video_handler.frames_number:
            raise Exception(f'The provided "resized_list" contains {str(len(resized_list))} elements and there are "{str(video_handler.frames_number)} frames.')
        if with_position_list is not None and len(with_position_list) != video_handler.frames_number:
            raise Exception(f'The provided "with_position_list" contains {str(len(resized_list))} elements and there are "{str(video_handler.frames_number)} frames.')
        if rotated_list is not None and len(rotated_list) != video_handler.frames_number:
            raise Exception(f'The provided "rotated_list" contains {str(len(resized_list))} elements and there are "{str(video_handler.frames_number)} frames.')
        
        # TODO: Remove this comment below if nothin else 
        # commented below that comment
        # I add frame_duration * 0.1 to make sure it fits the
        # next index
        if resized_list is not None:
            video = video.resized(lambda t: resized_list[video_handler.get_frame_number_by_time_moment(t)])
            #video = video.resized(lambda t: resized_list[int((t + frame_duration * 0.1) // frame_duration)])
        if with_position_list is not None:
            video = video.with_position(lambda t: with_position_list[video_handler.get_frame_number_by_time_moment(t)])
            #video = video.with_position(lambda t: with_position_list[int((t + frame_duration * 0.1) // frame_duration)])
        if rotated_list is not None:
            video = video.with_position(lambda t: rotated_list[video_handler.get_frame_number_by_time_moment(t)])
            #video = video.rotated(lambda t: rotated_list[int((t + frame_duration * 0.1) // frame_duration)])
        
        return CompositeVideoClip([
            background_video,
            video
        ])

