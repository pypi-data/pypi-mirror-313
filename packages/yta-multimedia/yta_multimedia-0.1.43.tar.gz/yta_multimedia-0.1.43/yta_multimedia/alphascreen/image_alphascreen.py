from yta_multimedia.alphascreen.masked_clip_creator import MaskedClipCreator
from yta_multimedia.image.region.image_region import ImageRegion
from yta_multimedia.image.region.image_region_finder import ImageRegionFinder
from yta_general_utils.image.checker import has_transparency
from yta_general_utils.file.checker import is_valid_image
from moviepy import ImageClip
from PIL import Image


class ImageAlphascreen:
    """
    Class to handle images with alphascreen regions and insert
    other images or videos on it.
    """
    image = None
    image_filename: str = None
    alpha_regions: list[ImageRegion] = []

    def __init__(self, filename: str):
        if not isinstance(filename, str):
            raise Exception(f'No str "filename" parameter "{filename}" provided.')
        
        if not is_valid_image(filename):
            raise Exception(f'The provided "filename" parameter "{filename}" is not a valid image.')
        
        image = Image.open(filename)

        if not has_transparency(image):
            raise Exception(f'The provided image "filename" parameter "{filename}" does not have any alpha channel.')

        self.image_filename = filename
        self.image = image
        self.alpha_regions = ImageRegionFinder.find_transparent_regions(self.image)

        if len(self.alpha_regions) == 0:
            raise Exception(f'No alpha regions found in the "filename" parameter "{filename}" provided.')
        
        # TODO: What about regions that are just one pixel or too short (?)

        # Duration will be processed and updated in the last step
        alpha_clip = ImageClip(self.image_filename, duration = 1 / 60)
        self.masked_clip_creator = MaskedClipCreator(self.alpha_regions, alpha_clip)
        
    def from_image_to_image(self, image, output_filename: str = None):
        """
        This method returns a numpy representation of the image
        built by inserting the provided 'image' in this alphascreen.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        # TODO: This is not returning RGBA only RGB
        return self.masked_clip_creator.from_image_to_image(image, output_filename)
    
    def from_images_to_image(self, images, output_filename: str = None):
        """
        This method returns a numpy representation of the image
        built by inserting the provided 'images' in this
        alphascreen.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        return self.masked_clip_creator.from_images_to_image(images, output_filename)
    
    def from_image_to_video(self, image, duration: float, output_filename: str = None):
        """
        This method returns a CompositeVideoClip with the provided
        'image' fitting the first alphascreen area and centered on
        those areas by applying a mask that let them be seen
        through that mask.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        return self.masked_clip_creator.from_images_to_video(image, duration, output_filename)

    def from_images_to_video(self, images, duration: float, output_filename: str = None):
        """
        This method returns a CompositeVideoClip with the provided
        'images' fitting the different alphascreen areas and
        centered on those areas by applying a mask that let them be
        seen through that mask.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        return self.masked_clip_creator.from_images_to_video(images, duration, output_filename)
    
    def from_video_to_video(self, video, output_filename: str = None):
        """
        This method returns a CompositeVideoClip with the provided
        'video' fitting in the alphascreen area and centered on it
        by applying a mask that let it be seen through that mask.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        return self.masked_clip_creator.from_video_to_video(video, output_filename)
    
    def from_videos_to_video(self, videos, output_filename: str = None):
        """
        This method returns a CompositeVideoClip with the provided
        'videos' fitting the different alphascreen areas and
        centered on those areas by applying a mask that let them be
        seen through that mask.

        This method will write the result as a local file if the
        'output_filename' parameter is provided.

        This method will work if the amount of images to insert is
        the same of the amount of transparent regions existing in 
        this alphascreen.
        """
        return self.masked_clip_creator.from_videos_to_video(videos, output_filename)