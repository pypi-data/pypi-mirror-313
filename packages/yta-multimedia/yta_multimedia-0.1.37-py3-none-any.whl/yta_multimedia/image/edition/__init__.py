from yta_multimedia.image.edition.filter.gameboy import image_file_to_gameboy
from yta_multimedia.image.edition.filter.pixelate import pixelate_image
from yta_multimedia.image.edition.filter.sticker import image_file_to_sticker


class ImageFilter:
    """
    Class to simplify and encapsulate the functionality related to
    applying filters to an image.
    """
    @staticmethod
    def to_gameboy(image_filename: str, output_filename: str):
        """
        Apply the original GameBoy colors palette to the provided
        'image_filename'.
        """
        # TODO: We need to refactor this when the original method
        # is also refactored
        return image_file_to_gameboy(image_filename, output_filename)
    
    @staticmethod
    def pixelate(image, i_size, output_filename: str):
        """
        Apply a pixelation of 'i_size' to the provided 'image'.
        """
        # TODO: Check that it is a valid image
        # TODO: Validate the provided 'i_size'
        return pixelate_image(image, i_size, output_filename)
    
    @staticmethod
    def to_sticker(image_filename: str, output_filename: str):
        """
        Turn the provided 'image_filename' into a sticker, which
        is the same image without the background and with a new
        white and wide border.
        """
        # TODO: Check that it is a valid 'image_filename'
        # TODO: Refactor to accept other image types, not only files
        return image_file_to_sticker(image_filename, output_filename)
    
    # TODO: Add 'image_to_sketch' if working, but I think it is
    # too heavy processing for nothing interesting...