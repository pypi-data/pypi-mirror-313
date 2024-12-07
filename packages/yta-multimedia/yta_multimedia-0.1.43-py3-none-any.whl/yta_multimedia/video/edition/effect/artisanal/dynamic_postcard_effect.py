from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.random import randrangefloat, random_bool
from moviepy import concatenate_videoclips, CompositeVideoClip, ColorClip, ImageClip
from moviepy.Clip import Clip


class DynamicPostcardEffect(Effect):
    """
    Makes the provided clip being displayed as a dynamic 
    postcard whose frames are rotated and resized to make
    an effect similar to the one in this reel:

    https://www.instagram.com/reel/C-ZzozroX_1/?igsh=MTVrcmtsYWFuMnowZw%3D%3D

    This effect is recommended to be used with a pure 
    white background.
    """
    def apply(self, video: Clip) -> Clip:
        background_video = ClipGenerator.get_default_background_video(duration = 1 / video.fps)

        return self.apply_over_video(video, background_video)
    
    def apply_over_video(self, video: Clip, background_video: Clip):
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        # TODO: We can use images as backgrounds if we have them
        # but we will have, for sure, dynamic white backgrounds
        # we create by ourselves
        #backgrounds_abspath = 'C:/Users/dania/Desktop/tmp_greenscreens/test_effect/'
        #files = FileHandler.get_list(backgrounds_abspath, FileSearchOption.FILES_ONLY)

        # I could obtain images from somewhere and resize all of them
        # to 1920x1080 keeping the aspect ratio

        # We need to have images enough for each video frame
        #images = files * (video.n_frames // len(files))

        frames = []
        for _, frame in enumerate(video.iter_frames()):
            # TODO: We can apply a stop-motion effect but that makes
            # the video last more than the original video
            frames.append(CompositeVideoClip([
                # TODO: What if 1920x1080 is not the original video size (?)
                ColorClip((1920, 1080), color = [255, 255, 255], duration = 1 / video.fps),
                # TODO: We can use the images as background instead of
                # these white backgrounds
                # ImageClip(images[index], duration = 5 / 60).with_fps(60),
                ImageClip(frame, duration = 1 / video.fps).with_fps(video.fps).with_position(('center', 'center'))
            ]))

        clips = []
        for frame in frames:
            #image_frame = ImageClip(frame, duration = 1 / 60).with_fps(60)
            resize = 1 + randrangefloat(0, 0.1, step = 0.005)
            rotation = 2 * randrangefloat(0, 1, step = 0.1)
            if random_bool():
                rotation = -abs(rotation)

            clips.append(CompositeVideoClip([
                ClipGenerator.get_default_background_video(duration = 1 / video.fps),
                #image_frame.with_position(('center', 'center')).resized(1 + randrangefloat(0, 0.1, step = 0.005)).rotated(rotation)
                frame.with_position(('center', 'center')).resized(resize).rotated(rotation)
            ]))

        # TODO: I think I am creating more clips than needed but,
        # as it seems to be working, I don't touch anything by now
        video = concatenate_videoclips(clips)
        # TODO: Do this as EaseIn or similar, not linear
        #white_background = ClipGenerator.generate_color_background((1920, 1080), [255, 255, 255], video.duration, video.fps)
        video = CompositeVideoClip([
            background_video,
            #ClipGenerator.get_default_background_video(duration = video.duration),
            video.resized(lambda t: 1.5 - 0.5 * t / video.duration).with_position(('center', 'center'))
        ])

        return video