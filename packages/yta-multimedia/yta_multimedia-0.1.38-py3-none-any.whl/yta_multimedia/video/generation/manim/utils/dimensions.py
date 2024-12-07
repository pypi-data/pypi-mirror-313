from yta_multimedia.video.generation.manim.constants import SCENE_HEIGHT, SCENE_WIDTH, STANDARD_HEIGHT, STANDARD_WIDTH
from manim import *


class ManimDimensions:
    """
    Class to encapsulate and simplify the functionality related to manim
    dimensions. Manim works with specific dimensions that are not measured
    in pixels and we use to work with pixels. This class was created to
    let us work with pixel dimensions that will be translated into manim
    dimensions to simplify the creative process.

    We consider that a manim screen has 1920x1080 dimensions in pixels, so
    those are the pixel dimensions you should keep in mind for your
    calculations.

    Manim dimensions system is (14 + 2/9)w x (8)h, which means that the 
    width is 14 + 2/9 and the height is 8. The upper left corner coordinate
    is [-7-1/9, 4, 0] (0 is the z axis), and the lower right corner 
    coordinate is [7+1/9, -4, 0], because the center of the scene and screen
    is the origin [0, 0, 0].
    """
    @staticmethod
    def width_to_manim_width(width: float):
        """
        Turns the pixel 'width' provided dimension to the corresponding manim
        width dimension. Remember that the system is prepared to work with a
        simulated screen of 1920x1080 pixels, so providing a 'width' of 1920
        will make the object fit the whole manim screen width.
        """
        return (width * SCENE_WIDTH) / STANDARD_WIDTH
    
    @staticmethod
    def manim_width_to_width(manim_width: float):
        """
        Turns the provided 'manim_width' dimension to the corresponding pixel
        width dimension based on our simulated screen size of 1920x1080 pixels.
        That means that providing a 'manim_width' of 14 + 2/9 will return 1920
        as pixel width, that is the screen size for our simulated whole screen.
        """
        # TODO: Maybe check if 'manim_width' is too big to raise
        # an exception or, at least, print a message
        return (manim_width * STANDARD_WIDTH) / SCENE_WIDTH
    
    @staticmethod
    def height_to_manim_height(height: float):
        """
        Turns the pixel 'height' provided dimension to the corresponding manim
        height dimension. Remember that the system is prepared to work with a
        simulated screen of 1920x1080 pixels, so providing a 'height' of 1080
        will make the object fit the whole manim screen height.
        """
        return (height * SCENE_HEIGHT) / STANDARD_HEIGHT
    
    @staticmethod
    def manim_height_to_height(manim_height: float):
        """
        Turns the provided 'manim_height' dimension to the corresponding pixel
        height dimension based on our simulated screen size of 1920x1080 pixels.
        That means that providing a 'manim_height' of 8 will return 1080 as
        pixel height, that is the screen size for our simulated whole screen.
        """
        # TODO: Maybe check if 'manim_height' is too big to raise
        # an exception or, at least, print a message
        return (manim_height * STANDARD_HEIGHT) / SCENE_HEIGHT



# TODO: Rename this
class ManimXGenerator:
    """
    Class to simplify and encapsulate the mobject generation functionality.
    """
    @staticmethod
    def mobject_fitting_width(mobject: Mobject, width: float, **kwargs):
        """
        Creates the provided 'mobject' with a size that fits the provided
        'width'. This will be limited to the height. If the new mobject
        height is greater than the screen max height, it will be limited
        to the height.

        If you want a mobject that just fits the provided 'width' ignoring
        the height, just use 'mobject.scale_to_fit_width(width)' instead.
        """
        width = ManimDimensions.width_to_manim_width(width)

        # We build both width and height fitted and get the most limited
        mobject_width_fitted = mobject(**kwargs).scale_to_fit_width(width)
        mobject_height_fitted = mobject(**kwargs).scale_to_fit_height(width)

        # As it is a 16:9 proportion, the height is the measure that limits the most
        if mobject_height_fitted.width < mobject_width_fitted.width:
            return mobject_height_fitted
        
        return mobject_width_fitted
    
    def mobject_fitting_height(mobject: Mobject, height: float, **kwargs):
        """
        Creates the provided 'mobject' with a size that fits the provided
        'height'. This will be limited to the width. If the new mobject
        width is greater than the screen max width, it will be limited
        to the width.

        If you want a mobject that just fits the provided 'height' ignoring
        the width, just use 'mobject.scale_to_fit_height(height)' instead.
        """
        height = ManimDimensions.height_to_manim_height(height)

        # We build both width and height fitted and get the most limited
        mobject_height_fitted = mobject(**kwargs).scale_to_fit_height(height)
        mobject_width_fitted = mobject(**kwargs).scale_to_fit_width(height)

        # As it is a 16:9 proportion, the height is the measure that limits the most
        # TODO: When it was Text the mobject I used the font.size to compare
        if mobject_height_fitted.width < mobject_width_fitted.width:
            return mobject_height_fitted
        
        return mobject_width_fitted
    
    def mobject_fitting_fullscreen(mobject: Mobject, **kwargs):
        """
        Creates the provided 'mobject' with a size to fit the whole screen.
        This method will return the provided 'mobject' fitting the standard
        whole screen. The mobject will be cropped if its aspect ratio is not 
        16:9, but it will fit the whole screen for sure.
        """
        image_width_fitted = mobject(**kwargs).scale_to_fit_width(ManimDimensions.width_to_manim_width(STANDARD_WIDTH))

        # We want the mobject that occupies the whole screen
        if ManimDimensions.manim_height_to_height(image_width_fitted.height) >= STANDARD_HEIGHT:
            return image_width_fitted
        
        image_height_fitted = mobject(**kwargs).scale_to_fit_height(ManimDimensions.height_to_manim_height(STANDARD_HEIGHT))

        return image_height_fitted
    
    def mobject_fitting_screen(mobject: Mobject, **kwargs):
        """
        Scales the provided 'mobject' if necessary to fit the screen. That 
        means that a mobject bigger than the screen size will be cropped
        to fit inside. One of the two dimensions (width or height) could
        be out of bounds if the provided 'mobject' is bigger than the 
        screen size when provided.
        """
        mobject = mobject(**kwargs)

        if ManimDimensions.manim_width_to_width(mobject.width) > STANDARD_WIDTH:
            mobject.scale_to_fit_width(ManimDimensions.width_to_manim_width(STANDARD_WIDTH))
        if ManimDimensions.manim_height_to_height(mobject.height) > STANDARD_HEIGHT:
            mobject.scale_to_fit_height(ManimDimensions.height_to_manim_height(STANDARD_HEIGHT))

    # TODO: Maybe we don't have to instantiate the mobject but resizing
    # it so 'mobject(**kwargs)' is not the way.


# TODO: You can do this below so you don't need to declare all args
# just pass the **kwargs and let the user build the 'color', 
# 'font_size' and all params he wants.
"""
kwargs = {
    'color': BLUE,
    'font_size': 22
}
self.play(Text('hola', **kwargs).animate.rotate(90 * DEGREES), run_time = 2)
"""

# TODO: Remove this below when refactored and unneeded
def fitting_text(text, width_to_fit: float = 1920, fill_opacity: float = 1, stroke_width: float = 0, color: ParsableManimColor = None, font_size: float = DEFAULT_FONT_SIZE, line_spacing: float = -1, font: str = '', slant: str = NORMAL, weight: str = NORMAL, t2c: dict[str, str] = None, t2f: dict[str, str] = None, t2g: dict[str, tuple] = None, t2s: dict[str, str] = None, t2w: dict[str, str] = None, gradient: tuple = None, tab_width: int = 4, warn_missing_font: bool = True, height: float = None, width: float = None, should_center: bool = True, disable_ligatures: bool = False, **kwargs):
    """
    This method returns a Text mobject that fits the provided 'width_to_fit'
    or, if the height is greater than the scene height, returns one with the
    greates possible width.
    
    This method has been built to be sure that your text is completely shown
    between the screen margins.

    @param
        **width_to_fit**
        The widht you want to fit, in normal pixels (1920 is the maximum). 
        These pixels will be processed to manim dimensions.
    """
    width_to_fit = ManimDimensions.width_to_manim_width(width_to_fit)

    txt_width_fitted = Text(text, fill_opacity, stroke_width, color, font_size, line_spacing, font, slant, weight, t2c, t2f, t2g, t2s, t2w, gradient, tab_width, warn_missing_font, height, width, should_center, disable_ligatures, **kwargs).scale_to_fit_width(width_to_fit)
    # I use a margin of 100 pixels so avoid being just in the borders
    txt_height_fitted = Text(text, fill_opacity, stroke_width, color, font_size, line_spacing, font, slant, weight, t2c, t2f, t2g, t2s, t2w, gradient, tab_width, warn_missing_font, height, width, should_center, disable_ligatures, **kwargs).scale_to_fit_height(SCENE_HEIGHT - ManimDimensions.height_to_manim_height(100))

    # As it is a 16:9 proportion, the height is the measure that limits the most
    if txt_height_fitted.font_size < txt_width_fitted.font_size:
        return txt_height_fitted
    return txt_width_fitted

def fitting_image(filename, width_to_fit, image_mode: str = 'RGBA', **kwargs):
    """
    Returns an ImageMobject of the provided 'filename' image that fits the provided 'width_to_fit'
    or, if the height limit is surpassed, that fits the height limit.

    @param
        **width_to_fit**
        The widht you want to fit, in normal pixels (1920 is the scene 
        width). These pixels will be processed to manim dimensions.
    """
    width_to_fit = ManimDimensions.width_to_manim_width(width_to_fit)

    image_width_fitted = ImageMobject(filename, image_mode, **kwargs).scale_to_fit_width(width_to_fit)
    image_height_fitted = ImageMobject(filename, image_mode, **kwargs).scale_to_fit_height(width_to_fit)

    # As it is a 16:9 proportion, the height is the measure that limits the most
    if image_height_fitted.width < image_width_fitted.width:
        return image_height_fitted
    
    return image_width_fitted

def fullscreen_image(filename, image_mode: str = 'RGBA', **kwargs):
    """
    Returns an ImageMobject that fits whole screen dimensions (1920x1080). It
    will ignore the dimension that is out of bounds.
    """
    image_width_fitted = ImageMobject(filename, image_mode, **kwargs).scale_to_fit_width(ManimDimensions.width_to_manim_width(1920))

    # We want the image that occupies the whole screen
    if ManimDimensions.manim_height_to_height(image_width_fitted.height) >= 1080:
        return image_width_fitted
    
    image_height_fitted = ImageMobject(filename, image_mode, **kwargs).scale_to_fit_height(ManimDimensions.height_to_manim_height(1080))

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