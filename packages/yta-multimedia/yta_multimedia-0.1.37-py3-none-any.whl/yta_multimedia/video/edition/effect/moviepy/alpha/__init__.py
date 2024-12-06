from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.numpy_frame_helper import FrameMaskingMethod
from yta_multimedia.video.frames.video_frame import VideoFrame
from moviepy import VideoClip
from typing import Union


class MoviepyAlphaTransitionHandler:
    """
    Class to handle the functionality related to turning
    alpha clips into moviepy mask clips to be able to 
    apply them and create affects and transitions.
    """
    @staticmethod
    def alpha_clip_to_mask_clip(video: Union[str, VideoClip], masking_method: FrameMaskingMethod = FrameMaskingMethod.PURE_BLACK_AND_WHITE):
        """
        The provided alpha 'video' is turned into a moviepy
        mask clip that can be set in any other video by
        using the '.with_mask()' method.

        If you apply the resulting mask to a clip (called 
        'video2' in below) then you can do this below to
        enjoy an incredible transition, or using a black
        background instead of the 'video1' in below.

        CompositeVideoClip([
            video,
            video2
        ]).write_videofile('alpha_masked_transition.mp4')
        """
        video = VideoParser.to_moviepy(video, True)
        masking_method = FrameMaskingMethod.to_enum(masking_method)

        transparent_pixel_in_mask = False
        if video.mask:
            for alpha_frame in video.mask.iter_frames():
                if (alpha_frame < 1.0).any():
                    transparent_pixel_in_mask = True

        # If mask has transparency, we keep the mask
        mask_clip = video.mask
        if not transparent_pixel_in_mask:
            mask_clip_frames = [VideoFrame(frame).as_mask(masking_method) for frame in video.iter_frames()]

            mask_clip = VideoClip(lambda t: mask_clip_frames[int(t * video.fps)], is_mask = True).with_fps(video.fps)

        return mask_clip