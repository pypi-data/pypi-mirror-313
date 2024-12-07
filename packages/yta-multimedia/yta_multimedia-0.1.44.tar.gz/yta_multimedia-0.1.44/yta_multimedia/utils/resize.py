from yta_general_utils.programming.parameter_validator import PythonValidator, NumberValidator


def get_cropping_points_to_keep_aspect_ratio(original_size: tuple, new_size: tuple):
    """
    This method calculates the upper left and bottom
    right corners point to be able to crop an element
    (video or image) to fit the 'new_size' aspect ratio.

    This method returns 2 values that are the points
    you need to use to crop your original element. These
    values are the top left corner and the bottom right
    corner.
    
    After cropping with this points you need to resize
    the element to the provided 'new_size' to get the
    desired element with the provided 'size'.
    """
    if not PythonValidator.is_tuple(original_size) or not PythonValidator.is_tuple(new_size) or len(original_size) != 2 or len(new_size) != 2:
        raise Exception('The provided "original_size" and/or "new_size" parameters are not tuples of 2 elements.')
    
    if not NumberValidator.is_positive_number(original_size[0]) or not NumberValidator.is_positive_number(original_size[1]) or not NumberValidator.is_positive_number(new_size[0]) or not NumberValidator.is_positive_number(new_size[1]):
        raise Exception('The provided "original_size" and/or "new_size" parameter do not contain positive values.')

    new_ratio = new_size[0] / new_size[1]
    # Get the dimensions of the sub-element we need to obtain,
    # by cropping, to fit the 'new_size' aspect ratio
    new_width, new_height = get_size_to_keep_aspect_ratio(original_size, new_ratio)

    # Lets get the points to crop the element
    # TODO: Maybe we need to make some calculations
    # to avoid odd numbers
    left = (new_width - new_size[0]) // 2
    top = (new_height - new_size[1]) // 2
    right = (new_width + new_size[0]) // 2
    bottom = (new_height + new_size[1]) // 2

    return (left, top), (right, bottom)

def get_size_to_keep_aspect_ratio(size: tuple, aspect_ratio: float):
    """
    This method will adjust the provided 'width' and 'height'
    to fit the provided 'aspect_ratio' using, as maximum, the
    provided 'width' or 'height' values.

    For example, if width = 900 and height = 900 and 
    aspect_ratio = 16/9, the result will be 900, 506.25 that
    are the values that fit the 'aspect_ratio' by using the
    'width' as it is (because it is the 'height' the one that
    has to be changed).

    This is useful when we need to fit some region of an 
    specific aspect ratio so we first adjust it and then resize
    it as needed.

    This method returns 2 values: the new width and height to
    fit the provided 'aspect_ratio' as width, height.
    """
    if not PythonValidator.is_tuple(size) or len(size) != 2:
        raise Exception('The provided "size" is not a tuple of 2 elements.')
    
    if not NumberValidator.is_positive_number(aspect_ratio):
        raise Exception('The provided "aspect_ratio" must be a positive number.')
    
    if not NumberValidator.is_positive_number(size[0]) or not NumberValidator.is_positive_number(size[1]):
        raise Exception('The provided "size" parameter does not contain positive values.')

    # TODO: What about non-int values (?)
    if size[0] / size[1] > aspect_ratio:
        new_height = size[1]
        new_width = new_height * aspect_ratio # Possible non-int
        
        if new_width > size[0]:
            new_width = size[0]
            new_height = new_width / aspect_ratio # Possible non-int
    else:
        new_width = size[0]
        new_height = new_width / aspect_ratio # Possible non-int
        
        if new_height > size[1]:
            new_height = size[1]
            new_width = new_height * aspect_ratio # Possible non-int

    return new_width, new_height