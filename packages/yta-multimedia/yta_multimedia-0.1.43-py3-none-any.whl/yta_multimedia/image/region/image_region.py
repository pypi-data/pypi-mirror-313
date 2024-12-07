from yta_multimedia.image.edition.resize import resize_image
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.resize import resize_video
from yta_general_utils.region import Region as BaseRegion
from yta_general_utils.image.parser import ImageParser


class ImageRegion(BaseRegion):
    """
    Class to represent a region built by two coordinates, one in
    the top left corner and another one in the bottom right 
    corner. This is useful to place an image inside the region.
    """
    def resize_image_to_fit_in(self, image):
        """
        This method rescales the provided 'image' to make it fit in
        this region. Once it's been rescaled, this image should be
        placed in the center of the region.
        """
        image = ImageParser.to_pillow(image)

        image = resize_image(image, (self.width, self.height))

        # We enlarge it by a 1% to avoid some balck pixels lines
        image = image.resize((image.size[0] * 1.01, image.size[1] * 1.01))

        return image
    
    # TODO: This could be private maybe
    # TODO: I should do this in yta_multimedia as it is
    # video related
    def resize_video_to_fit_in(self, video):
        """
        This method rescales the provided 'video' to make it fit in
        this region. Once it's been rescaled, this video should be
        placed in the center of the region.
        """
        video = VideoParser.to_moviepy(video)

        video = resize_video(video, (self.width, self.height))

        # We enlarge it by a 1% to avoid some black pixels lines
        video = video.resized(1.01)

        return video
    
    def place_video_inside(self, video):
        """
        This method rescales the provided 'video' to make it fit in
        this region. Once it's been rescaled, this videos is 
        positioned in the required position to fit the region.
        """
        video = self.resize_video_to_fit_in(video)

        x = (self.bottom_right.x + self.top_left.x) / 2 - video.w / 2
        y = (self.bottom_right.y + self.top_left.y) / 2 - video.h / 2

        # TODO: What about upper limits (out of bottom left bounds) (?)
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        video = video.with_position((x, y))

        return video