from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWith, MoviepyArgument
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_general_utils.math.rate_functions import RateFunction
from moviepy.Clip import Clip
from typing import Union


class ShakeAtPositionEffect(Effect):
    def apply(self, video: Clip, position: Union[Position, Coordinate, tuple] = Position.CENTER) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        background_video = ClipGenerator.get_default_background_video()

        return self.apply_over_video(video, background_video, position)
    
    # TODO: What about this (?)
    def apply_over_video(self, video: Clip, background_video: Clip, position: Union[Position, Coordinate] = Position.CENTER) -> Clip:
        arg = MoviepyArgument(position, position, TFunctionSetPosition.linear_with_normal_shaking, RateFunction.linear)

        return MoviepyWith().apply_over_video(video, background_video, with_position = arg)
    

# TODO: I kee this code below just for a few commits to
# be able to think about its structure and check the
# difference with the one above
# class ShakeAtPosition(Effect):
#     """
#     This effect will blur the whole clip. The greater the
#     'blur_radius' is, the more blurred it becomes.
#     """
#     def apply(self, video: Clip, position: Union[Position, Coordinate, tuple] = Position.CENTER) -> Clip:
#         # TODO: This is not working properly yet
#         #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
#         background_video = ClipGenerator.get_default_background_video()

#         return self.apply_over_video(video, background_video, position)
    
#     # TODO: What about this (?)
#     def apply_over_video(self, video: Clip, background_video: Clip, position: Union[Position, Coordinate] = Position.CENTER) -> Clip:
#         video = VideoParser.to_moviepy(video)
#         background_video = VideoParser.to_moviepy(background_video)

#         # TODO: Validate position

#         if PythonValidator.is_tuple(position):
#             position = Coordinate(position[0], position[1])

#         # Turn position into upper left moviepy position
#         if PythonValidator.is_instance(position, Position):
#             position = position.get_moviepy_upper_left_corner_tuple(video.size, background_video.size)
#         elif PythonValidator.is_instance(position, Coordinate):
#             position = position.get_moviepy_upper_left_corner_tuple(video.size, background_video.size)

#         video_handler = VideoHandler(video)
#         background_video = video_handler.prepare_background_clip(background_video)

#         # TODO: What if I want to shake it while moving (?)

#         video = video.with_position(lambda t: shake_movement(t, position[0], position[1])).with_start(0).with_duration(video.duration)
        
#         return CompositeVideoClip([
#             background_video,
#             video
#         ])