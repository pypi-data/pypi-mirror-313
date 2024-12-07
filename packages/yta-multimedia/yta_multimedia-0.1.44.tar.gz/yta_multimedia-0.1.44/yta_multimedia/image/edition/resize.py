from yta_multimedia.utils.resize import get_cropping_points_to_keep_aspect_ratio
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.image.converter import ImageConverter
from yta_general_utils.programming.output import handle_output_filename
from PIL import Image
from typing import Union, Any

import numpy as np
import cv2


# TODO: Refactor and encapsulate in a class
def resize_image(image: Union[str, Any], size, output_filename: Union[str, None] = None):
    """
    Resizes the image to the provided 'size' by cropping a
    region of the given 'image' that fits the 'size' aspect
    ratio and resizing that region to the 'size'.

    This method is using the whole image and then resizing,
    so the quality of the image is preserved and no small
    regions are used. The most part of the image is 
    preserved.

    This method returns the image modified.

    This method will write the image if 'output_filename' is
    provided.
    """
    image = ImageParser.to_pillow(image)

    top_left, bottom_right = get_cropping_points_to_keep_aspect_ratio(image.size, size)
    image = image.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
    image = image.resize(size)

    output_filename = handle_output_filename(output_filename, 'png')
    if output_filename:
        image.save(output_filename)

    return image

# TODO: Are these methods below interesting or even used (?) I think
# they can be done with libraries .resize methods...
# TODO: Make 'image: Union[str, Image.Image, np.ndarray]' work please
def resize_image_scaling(image: Union[str, Any], width: int, height: int, output_filename: Union[str, None] = None):
    """
    Resizes the provided 'image' (if valid) to the provided dimensions
    ('width', 'height') scaling it (losing not the aspect ratio). The
    image will be stored locally as 'output_filename' if provided and
    will be returned once it's been scalled, in any case.

    TODO: Please, test and check this method
    """
    # TODO: This method needs to be checked properly
    if not image:
        raise Exception('No "image" provided.')

    if not width:
        raise Exception('No "width" provided.')
    
    if not height:
        raise Exception('No "height" provided.')

    if PythonValidator.is_string(image):
        # TODO: Check if image is actually an image
        image = Image.open(image)

    if PythonValidator.is_numpy_array(image):
        image = ImageConverter.numpy_image_to_pil(image)

    # Lets resize it
    image_width, image_height = image.size

    if image_width == width and image_height == height:
        return image.save(output_filename)

    aspect_ratio = image_width / image_height
    if aspect_ratio > (width / height):
        # Image is very horizontal, so width changes faster, we need to focus on height
        factor = (height * 100 / image_height) / 100
        image_width = int(image_width * factor)
        image_height = height
    else:
        # Image is very vertical, so height changes faster, we need to focus on width
        factor = (width * 100 / image_width) / 100
        image_width = 1920
        image_height = int(image_height * factor)
    image = image.resize((image_width, image_height))

    # We will crop form the center to edges
    left = 0
    right = width
    if image_width > width:
        # If it is 1960 => leave [0, 20], get [20, 1940], leave [1940, 1960]
        margin = int((image_width - width) / 2)
        left = 0 + margin
        right = image_width - margin
        # We make and adjustment if some pixel left
        while (right - left) > width:
            right -= 1
        while (right - left) < width:
            if left > 0:
                left -= 1
            else:
                right += 1

    top = 0
    bottom = height
    if image_height > height:
        # If it is 1140 => leave [0, 30], get [30, 1110], leave [1110, 1140]
        margin = int((image_height - height) / 2)
        top = 0 + margin
        bottom = image_height - margin
        # We make and adjustment if some pixel left
        while (bottom - top) > height:
            bottom -= 1
        while (bottom - top) < height:
            if top > 0:
                top -= 1
            else:
                bottom += 1

    # Image that is 1920x1080 and is the center of the original image
    image = image.crop((left, top, right, bottom))

    if output_filename:
        image.save(output_filename)

    return image

def resize_image_without_scaling(image: Union[str, Any], width: int, height: int, output_filename: Union[str, None] = None):
    """
    Resizes the provided 'image' (if valid) to the provided dimensions
    ('width', 'height') guaranteen not that the aspect ratio is kept. 
    The image will be stored locally as 'output_filename' if provided
    and will be returned once it's been scalled, in any case.

    TODO: Please, test and check this method
    """
    # TODO: This method needs to be checked properly
    if not image:
        raise Exception('No "image" provided.')

    if not width:
        raise Exception('No "width" provided.')
    
    if not height:
        raise Exception('No "height" provided.')

    if PythonValidator.is_string(image):
        # TODO: Check if image is actually an image
        image = Image.open(image)

    if PythonValidator.is_numpy_array(image):
        image = ImageConverter.numpy_image_to_pil(image)

    # From here: https://stackoverflow.com/a/14140796
    image = image.convert('RGB')
    image = np.array(image) # To cv2
    image = image[:, :, ::-1].copy() # Convert RGB to BGR

    #image = cv2.imread(image_filename)
    resized_image = cv2.resize(image, dsize = (width, height), interpolation = cv2.INTER_CUBIC)

    if output_filename:
        cv2.imwrite(output_filename, resized_image)

    return resized_image


# TODO: Remove these 2 methods below if the ones above are working, because
# they are more general (using different types or images)
def resize_image_file_scaling(image_filename: str, width: int, height: int, output_filename = None):
    """
    Resizes the provided 'image_filename' to the provided 'width' and 'height' keeping the
    aspect ratio. This method enlarges the image to fit the desired size and then makes a 
    crop to obtain that size from the center of the resized image. If 'output_filename' is
    provided, the image is saved locally with that name. If not, it is only returned
    """
    if not image_filename:
        return None
    
    # TODO: Do some checkings on width and height (?)

    # TODO: This is not working well when '' passed
    if output_filename is not None and not output_filename:
        return None

    image = Image.open(image_filename)
    image_width, image_height = image.size

    if image_width == width and image_height == height:
        return image.save(output_filename)

    aspect_ratio = image_width / image_height
    if aspect_ratio > (width / height):
        # Image is very horizontal, so width changes faster, we need to focus on height
        factor = (height * 100 / image_height) / 100
        image_width = int(image_width * factor)
        image_height = height
    else:
        # Image is very vertical, so height changes faster, we need to focus on width
        factor = (width * 100 / image_width) / 100
        image_width = 1920
        image_height = int(image_height * factor)
    image = image.resize((image_width, image_height))

    # We will crop form the center to edges
    left = 0
    right = width
    top = 0
    bottom = height
    if image_width > width:
        # If it is 1960 => leave [0, 20], get [20, 1940], leave [1940, 1960]
        margin = int((image_width - width) / 2)
        left = 0 + margin
        right = image_width - margin
        # We make and adjustment if some pixel left
        while (right - left) > width:
            right -= 1
        while (right - left) < width:
            if left > 0:
                left -= 1
            else:
                right += 1
    if image_height > height:
        # If it is 1140 => leave [0, 30], get [30, 1110], leave [1110, 1140]
        margin = int((image_height - height) / 2)
        top = 0 + margin
        bottom = image_height - margin
        # We make and adjustment if some pixel left
        while (bottom - top) > height:
            bottom -= 1
        while (bottom - top) < height:
            if top > 0:
                top -= 1
            else:
                bottom += 1

    image = image.crop((left, top, right, bottom))
    # Image that is 1920x1080 and is the center of the original image
    if output_filename:
        image.save(output_filename)

    return image