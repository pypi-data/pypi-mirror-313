from PIL import Image


# TODO: Do we need this (?)
# TODO: Refactor these 2 methods in one
def image_file_has_transparency(image_filename: str):
    """
    Checks if the provided 'image_filename' has transparency or not.
    This method returns True if yes or False if not.
    """
    if not image_filename:
        return None
    
    if not image_file_is_valid(image_filename):
        return None
    
    return image_has_transparency(Image.open(image_filename))

def image_has_transparency(image: Image):
    """
    Checks if the provided image (read with pillow) has transparency.
    This method returns True if yes or False if not.
    """
    if image.info.get("transparency", None) is not None:
        return True
    if image.mode == "P":
        transparent = image.info.get("transparency", -1)
        for _, index in image.getcolors():
            if index == transparent:
                return True
    elif image.mode == "RGBA":
        extrema = image.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def image_file_is_valid(image_filename: str):
    """
    Tries to open the 'image_filename' provided to check if it is corrupt or it is valid. It 
    returns True if the provided image is valid, or False if is corrupt.

    # TODO: Maybe move this to 'yta-general-utils' (?)
    """
    if not image_filename:
        return None
    
    if not image_file_is_valid(image_filename):
        return None

    try:
        im = Image.open(image_filename)
        im.verify()
        im.close()
    except (IOError, OSError, Image.DecompressionBombError) as e:
        return False
    
    return True