from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import ImageClip
from typing import Union, Any


# TODO: I don't know if I should put this in another file or not...
# effect: segments.building.objects.effect.Effect = None
def generate_video_from_image(image: Union[str, Any], duration = 1, effect = None):
    """
    Genearates a ImageClip with the provided 'image_filename' that lasts the also
    provided 'duration'.

    This method will internally apply the 'effect' if provided. Check code or 
    developer guide to see available effects.
    """
    if image is None:
        raise Exception('No "image" provided.')

    # if variable_is_type(image, str):
    #     # TODO: Check if image is actually an image
    #     # TODO: This image throws 'AttributeError: shape' moviepy error
    #     image = Image.open(image)
    # elif variable_is_type(image, np.ndarray):
    #     image = numpy_image_to_pil(image)

    if not PythonValidator.is_string(image):
        # TODO: Do something
        pass

    slide = ImageClip(image, duration = duration)
    slide = slide.with_fps(60)

    # TODO: This need work
    #slide = apply_effect(slide, effect)

    return slide