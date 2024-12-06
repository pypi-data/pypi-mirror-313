from yta_general_utils.temp import create_temp_filename
from yta_general_utils.image.parser import ImageParser
from PIL import Image


def pixelate_image(image, i_size, output_filename: str):
    """
    Pixelates the provided 'image' and saves it as the 'output_filename' if
    provided.
    The 'i_size' is the pixelating square. The smaller it is, the less pixelated 
    its.

    'i_size' must be a tuple such as (8, 8) or (16, 16).
    """
    img = ImageParser.to_pillow(image)

    # Convert to small image
    small_img = img.resize(i_size, Image.BILINEAR)

    # Resize to output size
    res = small_img.resize(img.size, Image.NEAREST)

    # TODO: Validate 'output_filename' if provided
    if not output_filename:
        output_filename = create_temp_filename('tmp_sketch.png')
        
    # TODO: Return it instead of saving
    res.save(output_filename)