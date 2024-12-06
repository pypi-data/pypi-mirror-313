from yta_multimedia.image.edition.filter.workers.sketch.linedraw import apply_line_sketch_to_image
from yta_general_utils.image.converter import ImageConverter
from PIL import Image
from typing import Union

import cv2
import numpy as np


def image_to_sketch(image: str, output_filename: Union[str, None] = None):
    """
    Turns the provided 'image' into an sketch that is made 
    by white and black colors.
    """
    # Thank you: https://github.com/code-kudos/Convert-any-image-to-sketch-with-python/blob/main/Sketch.py
    # TODO: Image can be an array containing the image (numpy.ndarray)
    # TODO: Check if image provided is # numpy.ndarray or PIL image
    # if not image:
    #     return None

    # TODO: Check 'output_filename'
    # if isinstance(image, np.ndarray):
    #     image = ImageConverter.numpy_image_to_pil(image)
    # else:
    #     # TODO: Check if image is actually a Image.opened(image)
    #     image = Image.open(image)

    # numpy array is working here
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert_img = cv2.bitwise_not(grey_img)
    blur_img = cv2.GaussianBlur(invert_img, (277, 277), 0)
    invblur_img = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(grey_img, invblur_img, scale = 256.0)
    rgb_sketch = cv2.cvtColor(sketch_img, cv2.COLOR_BGR2RGB)

    sketch_image = Image.fromarray(rgb_sketch)

    if output_filename:
        sketch_image.save(output_filename)

    return sketch_image

def image_to_line_sketch(image: str, output_filename: Union[str, None] = None):
    """
    Turns the provided 'image' into an line sketch that is made 
    by white and black colors.
    """
    # Thank you: https://github.com/LingDong-/linedraw
    # TODO: Image can be an array containing the image (numpy.ndarray)
    # TODO: Check if image provided is # numpy.ndarray or PIL image
    # if not image:
    #     return None

    # Code here below:
    # TODO: I think the 'output_filename' here is not needed
    sketch_image = apply_line_sketch_to_image(image, output_filename)

    if output_filename:
        sketch_image.save(output_filename)

    return sketch_image