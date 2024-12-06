from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_multimedia.greenscreen.custom.utils import get_greenscreen_details
from yta_multimedia.alphascreen.masked_clip_creator import MaskedClipCreator
from yta_multimedia.greenscreen.enums import GreenscreenType
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoClip, VideoFileClip
from moviepy.video.fx import MaskColor
from typing import Union


class VideoGreenscreen:
    """
    Class representing a Video with some greenscreen regions on it
    that can be used to place other resources (images or videos)
    fitting those regions while this greenscreen video is displayed.

    This class is working as if the greenscreen regions in the image
    were static, so if it moves this won't work properly as it is 
    not mapping the region for all the frames, just for the first 
    one.

    TODO: Improve this by autodetecting all the greenscreen regions
    for each frame and storing them somewhere.
    """
    greenscreen: GreenscreenDetails = None
    """
    This parameter keeps the information about the greenscreen 
    regions that the video has, including their corner coordinates,
    the width, the height and the green color to apply the mask.
    """

    def __init__(self, greenscreen: Union[GreenscreenDetails, str]):
        # TODO: Enhance this by detecting greenscreens for each frame
        if PythonValidator.is_string(greenscreen):
            # We need to automatically detect greenscreen details
            greenscreen = get_greenscreen_details(greenscreen, GreenscreenType.VIDEO)

        self.greenscreen = greenscreen

        # TODO: Do this here to be able to use it in the masked_clip_creator
        TMP_FILENAME = self.greenscreen.get_filename()
        # I consider the same greenscreen rgb color for all areas
        greenscreen_clip = VideoFileClip(TMP_FILENAME).with_effects([MaskColor(color = self.greenscreen.greenscreen_areas[0].rgb_color, threshold = 100, stiffness = 5)])

        regions = [gsa.region for gsa in self.greenscreen.greenscreen_areas]

        self.masked_clip_creator = MaskedClipCreator(regions, greenscreen_clip)
       
    def from_image_to_image(self, image, output_filename: str):
        """
        Receives an 'image', places it into the greenscreen and generates
        an image with the first clip that is stored locally as
        'output_filename' if provided.
        """
        # TODO: This is not returning RGBA only RGB
        return self.masked_clip_creator.from_image_to_image(image, output_filename)
    
    def from_images_to_image(self, images, output_filename: str):
        return self.masked_clip_creator.from_images_to_image(images, output_filename)
    
    def from_image_to_video(self, image, duration: float, output_filename: str):
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
        """
        Puts the provided 'videos' inside the greenscreen region by
        applying a mask, cropping the videos if necessary and rescaling
        them, also positioning to fit the region and returns the 
        CompositeVideoClip created.

        Videos can be longer or shorter than greenscreen clip. By now
        we are making that all videos fit the greenscreen duration. 
        That is achieved by enlarging or shortening them if necessary.
        Thats why results could be not as expected.

        TODO: Please, build some different strategies to apply here.
        """
        return self.masked_clip_creator.from_videos_to_video(videos, output_filename)