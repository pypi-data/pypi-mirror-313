from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_multimedia.greenscreen.custom.utils import get_greenscreen_details
from yta_multimedia.alphascreen.masked_clip_creator import MaskedClipCreator
from yta_multimedia.greenscreen.enums import GreenscreenType
from yta_general_utils.programming.parameter_validator import PythonValidator
from typing import Union
from moviepy import ImageClip, VideoClip
from moviepy.video.fx import MaskColor
from PIL import Image, ImageDraw
from typing import Union


class ImageGreenscreen:
    greenscreen: GreenscreenDetails = None

    def __init__(self, greenscreen: Union[GreenscreenDetails, str]):
        if PythonValidator.is_string(greenscreen):
            # We need to automatically detect greenscreen details
            greenscreen = get_greenscreen_details(greenscreen, GreenscreenType.IMAGE)

        self.greenscreen = greenscreen

        # TODO: Do this here to be able to use it in the masked_clip_creator
        TMP_FILENAME = self.greenscreen.get_filename()
        # I consider the same greenscreen rgb color for all areas
        # Duration will be set at the end
        greenscreen_clip = ImageClip(TMP_FILENAME, duration = 1 / 60).with_effects([MaskColor(color = self.greenscreen.greenscreen_areas[0].rgb_color, threshold = 100, stiffness = 5)])
        
        regions = [gsa.region for gsa in self.greenscreen.greenscreen_areas]

        self.masked_clip_creator = MaskedClipCreator(regions, greenscreen_clip)

    def __process_elements_and_save(self, output_filename):
        """
        Processes the greenscreen by writing the title, description
        and any other available element, and stores it locally as
        'output_filename' once processed.
        """
        base = Image.open(self.greenscreen.filename_or_google_drive_url)
        draw = ImageDraw.Draw(base)

        # TODO: I preserve this code for the future
        # # We need to write title if existing
        # if self.__title:
        #     title_position = (self.__title_x, self.__title_y)
        #     draw.text(title_position, self.__title, font = self.__title_font, fill = self.__title_color)

        # if self.__description:
        #     description_position = (self.__description_x, self.__description_y)
        #     draw.text(description_position, self.__description, font = self.__description_font, fill = self.__description_color)

        # TODO: Handle anything else here

        # We save the image
        base.save(output_filename, quality = 100)

    def from_image_to_image(self, image, output_filename: Union[str, None] = None):
        """
        Receives an 'image', places it into the greenscreen and generates
        another image that is stored locally as 'output_filename' if
        provided.
        """
        # TODO: This is not returning RGBA only RGB
        return self.masked_clip_creator.from_image_to_image(image, output_filename)

    def from_images_to_image(self, images, output_filename: str = None):
        return self.masked_clip_creator.from_images_to_image(images, output_filename)

    def from_image_to_video(self, image, duration: float, output_filename: Union[str, None] = None):
        """
        Receives an 'image', places it into the greenscreen and generates
        a video of 'duration' seconds of duration that is returned. This method
        will store locally the video if 'output_filename' is provided.
        """
        return self.masked_clip_creator.from_image_to_video(image, duration, output_filename)

    def from_images_to_video(self, images, duration: float, output_filename: str = None):
        return self.masked_clip_creator.from_images_to_video(images, duration, output_filename)
    
    def from_video_to_video(self, video: Union[str, VideoClip], output_filename: str = None):
        """
        Inserts the provided 'video' in the greenscreen and returns the
        CompositeVideoClip that has been created. If 'output_filename' 
        provided, it will be written locally with that file name.

        The provided 'video' can be a filename or a moviepy video clip.
        """
        return self.masked_clip_creator.from_video_to_video(video, output_filename)
    
    def from_videos_to_video(self, videos: list[Union[str, VideoClip]], output_filename: str = None):
        return self.masked_clip_creator.from_videos_to_video(videos, output_filename)