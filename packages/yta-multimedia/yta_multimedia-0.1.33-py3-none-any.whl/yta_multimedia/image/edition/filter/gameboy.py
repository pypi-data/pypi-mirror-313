import cv2
import scipy.spatial as sp


# TODO: Refactor this to work with non-file images and
# write image only if 'output_filename' is provided.
def image_file_to_gameboy(image_filename: str, output_filename: str):
    """
    Receives an 'image_filename' and turns it into a game boy
    art (turning it into the game boy screen pixel colors) and
    saves it as 'output_filename'.

    The input file image will be resized to (480, 432), that is
    the game boy screen size.

    # TODO: Make this method work within a video (maybe with
    pygame) and set the code in video.edition section
    """
    if not image_filename:
        return None
    
    if not output_filename:
        return None

    # These below are the colors used in GB
    GAMEBOY_COLORS = [
        (155, 188, 15),
        (139, 172, 15),
        (48, 98, 48),
        (15, 56, 15),
        (15, 56, 15)
    ]

    # Original gameboy screen size is (480, 432)
    image = cv2.imread(image_filename)
    image = cv2.resize(image, (480, 432)) 
    rows, cols, _ = image.shape
    new_image = image.copy()

    """
    TODO: Improve this method. 
    
    Scroll the whole image, but do one step first. Check
    in a list if the pixel is written. If not, look for
    the nearest rgb color and store it in that list. Then
    write it in the new image. If found, you don't need 
    to look for the nearest (through tree.query) again.
    You just need to look for it in the list.

    Or maybe that doesn't make it faster. Don't know.
    """

    tree = sp.KDTree(GAMEBOY_COLORS)
    for i in range(rows):
        for j in range(cols):
            pixel_color = image[i, j]
            distance, result = tree.query(pixel_color) 
            nearest_color = GAMEBOY_COLORS[result]
            new_image[i, j] = nearest_color

    cv2.imwrite(output_filename, new_image)
    print(output_filename + ' written successfully.')
