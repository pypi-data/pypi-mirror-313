from yta_multimedia.video.generation.manim.constants import SCENE_HEIGHT
from yta_multimedia.video.generation.manim.utils.dimensions import ManimDimensions
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.temp import create_temp_filename
from moviepy import AudioFileClip
from manim import *


"""
Docummentation here: 
    https://docs.manim.community/en/stable/

Useful links:
- https://www.youtube.com/watch?v=KHGoFDB-raE (+1h of using SVGs and drawing and animating)
- https://www.youtube.com/watch?v=bCsk6hnMO5w   (Mobjects and animations)
            -> https://github.com/mphammer/Manim-Mobjects-and-Animations/blob/main/animations.py
- https://www.youtube.com/watch?v=5qj3b7DY5oA   (Mobjects and animations)
            -> https://github.com/mphammer/Manim-Mobjects-and-Animations/blob/main/mobjects.py

Command to throw:
    manim PYTHON_FILE.py CLASS_NAME -pqm
"""

"""
Interesting:
    - https://docs.manim.community/en/stable/examples.html (some examples)
    - https://medium.com/@andresberejnoi/data-visualization-bar-chart-animations-with-manim-andres-berejnoi-75ece91a2da4 (bar graphs)
"""

# TODO: Is all this needed (?)
def manim_alpha_animation_to_videoclip(video):
    """
    Reads the provided 'video' manim generated .mov animation,
    makes the audio fix and returns a VideoFileClip object to
    work with.

    I don't know how o where this bug is done, but when using
    directly a alpha manim animation that has any sound, with
    the moviepy library, the final audio is different and
    doesn't fit the original timing.

    This method extracts the original audio, turns it into a
    new mp3 file and set that new audio file as the video 
    audio, apparently fixing the bug.
    """
    video = VideoParser.to_moviepy(video, do_include_mask = True)

    MP3_EXPORTED_FILENAME = create_temp_filename('manim_exported_audio.mp3')
    video.audio.write_audiofile(MP3_EXPORTED_FILENAME)

    try:
        # Extract the audio
        #AudioSegment.from_file(video_filename).export(MP3_EXPORTED_FILENAME, format = 'mp3')

        # Replace the original audio in moviepy video with this extracted one
        video.audio = AudioFileClip(MP3_EXPORTED_FILENAME)
    except:
        pass

    return video

# TODO: Maybe this one needs to be moved to a text handler
def fitting_text(text, width_to_fit: float = 1920, fill_opacity: float = 1, stroke_width: float = 0, color: ParsableManimColor = None, font_size: float = DEFAULT_FONT_SIZE, line_spacing: float = -1, font: str = '', slant: str = NORMAL, weight: str = NORMAL, t2c: dict[str, str] = None, t2f: dict[str, str] = None, t2g: dict[str, tuple] = None, t2s: dict[str, str] = None, t2w: dict[str, str] = None, gradient: tuple = None, tab_width: int = 4, warn_missing_font: bool = True, height: float = None, width: float = None, should_center: bool = True, disable_ligatures: bool = False, **kwargs):
    width_to_fit = ManimDimensions.width_to_manim_width(width_to_fit)

    txt_width_fitted = Text(text, fill_opacity, stroke_width, color, font_size, line_spacing, font, slant, weight, t2c, t2f, t2g, t2s, t2w, gradient, tab_width, warn_missing_font, height, width, should_center, disable_ligatures, **kwargs).scale_to_fit_width(width_to_fit)
    # I use a margin of 100 pixels so avoid being just in the borders
    txt_height_fitted = Text(text, fill_opacity, stroke_width, color, font_size, line_spacing, font, slant, weight, t2c, t2f, t2g, t2s, t2w, gradient, tab_width, warn_missing_font, height, width, should_center, disable_ligatures, **kwargs).scale_to_fit_height(SCENE_HEIGHT - ManimDimensions.height_to_manim_height(100))

    # As it is a 16:9 proportion, the height is the measure that limits the most
    if txt_height_fitted.font_size < txt_width_fitted.font_size:
        return txt_height_fitted
    return txt_width_fitted

def fullscreen_image(filename, scale_to_resolution: int = QUALITIES[DEFAULT_QUALITY]["pixel_height"], invert: bool = False, image_mode: str = 'RGBA', **kwargs):
    """
    Returns an ImageMobject that fits the provided 'width_to_fit' ignoring height. This is useful
    if you want an Image that fills the whole screen width.
    """
    image_width_fitted = ImageMobject(filename, scale_to_resolution, invert, image_mode, **kwargs).scale_to_fit_width(ManimDimensions.width_to_manim_width(1920))
    image_height_fitted = ImageMobject(filename, scale_to_resolution, invert, image_mode, **kwargs).scale_to_fit_height(ManimDimensions.height_to_manim_height(1080))

    # We want the image that occupies the whole screen
    if ManimDimensions.manim_height_to_height(image_width_fitted.height) >= 1080:
        return image_width_fitted
    
    return image_height_fitted

def preprocess_image(image: ImageMobject):
    """
    This method processes images bigger than our 1920x1080 dimensions and returns it
    scaled down to fit those dimensions. You should use this method as the first one
    when working with ImageMobjects, and then scaling it down as much as you need.
    """
    if ManimDimensions.manim_width_to_width(image.width) > 1920:
        image.scale_to_fit_width(ManimDimensions.width_to_manim_width(1920))
    if ManimDimensions.manim_height_to_height(image.height) > 1080:
        image.scale_to_fit_height(ManimDimensions.height_to_manim_height(1080))

    return image

# TODO: Remove this below as it is useless
# def add_manim_animation_to_video(original_video_filename, original_video_duration, manim_animation_name, manim_animation_parameters, output_filename):
#     """
#     Generates a manim animation video file with the provided 'manim_animation_name' and
#     'manim_animation_parameters', and puts it in the foreground of the original video
#     provided.

#     'original_video_duration' parameter is passed to crop the original video to that
#     duration in seconds if it is interesting for the final animation.

#     This is a method that must be used to add any manim animation to any app-generated
#     video.
#     """
#     from utils.video_utils import add_manin_animation_to_video as add_manim_animation_to_videoclip
#     TMP_MANIM_ANIMATION_FILENAME = PROJECT_ABSOLUTE_PATH + 'tmp_manim_animation.mov'

#     # TODO: Check that 'manim_animation_name' exist (is valid)

#     # We generate the animation video file
#     generate_manim_animation(manim_animation_name, manim_animation_parameters, TMP_MANIM_ANIMATION_FILENAME)

#     # We put the animation video file in the foreground of the original video
#     add_manim_animation_to_videoclip(original_video_filename, original_video_duration, TMP_MANIM_ANIMATION_FILENAME, output_filename)
    
# TODO: Is this below useful?
# export with transparent background: https://manimclass.com/manim-export-transparent-background/
# command to export:   manim --format=mp4 -qm -t Formula
