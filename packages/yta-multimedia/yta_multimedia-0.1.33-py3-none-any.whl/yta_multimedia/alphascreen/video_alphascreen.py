from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.alphascreen.masked_clip_creator import MaskedClipCreator
from yta_general_utils.image.region import ImageRegionFinder, Region


# TODO: This class has not been tested yet with real alpha videos
class VideoAlphascreen:
    """
    Class to handle videos with alphascreen regions and insert
    other videos or images on it.
    """
    video = None
    alpha_regions: list[Region] = []

    def __init__(self, video: str):
        video = VideoParser.to_moviepy(video, do_include_mask = True)

        # TODO: Check that video mask has some transparency

        self.video = video
        # TODO: Import from 'frames' the 'get_frame_from_video_as_rgba_by_frame_number(0)'
        self.alpha_regions = ImageRegionFinder.find_transparent_regions(VideoFrameExtractor.get_frame_as_rgba_by_time(video, 0))

        if len(self.alpha_regions) == 0:
            raise Exception('No alpha regions found in the "filename" parameter "{filename}" provided.')
        
        # TODO: What about regions that are just one pixel or too short (?)

        alpha_clip = self.video
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
        return self.masked_clip_creator.from_image_to_video(image, duration, output_filename)

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