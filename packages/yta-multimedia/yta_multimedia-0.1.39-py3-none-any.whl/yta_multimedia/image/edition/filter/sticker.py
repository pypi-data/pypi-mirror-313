from yta_multimedia.image.edition.background import remove_image_background
from yta_general_utils.temp import create_temp_filename
from PIL import Image

import numpy as np
import cv2


# TODO: Refactor this to accept not only image files
def image_file_to_sticker(image_filename: str, output_filename: str):
    """
    Receives an image and turns it into an sticker. This method will remove the 
    background of the provided 'image_filename' and surrounds the main object
    in that picture with a wide white border (as social networks stickers). It 
    will also crop the image to fit the remaining object only.
    """
    # From here: https://withoutbg.com/resources/creating-sticker
    if not image_filename:
        return None
    
    # TODO: Validate and improve the way we handle 'output_filename'
    if not output_filename:
        return None

    # We enlarge the image 40 pixels (each border) to ensure sticker works well
    # TODO: Move this to a custom method
    enlarged_filename = create_temp_filename('enlarged.png')
    old_im = Image.open(image_filename)
    old_size = old_im.size

    new_size = (old_size[0] + 80, old_size[1] + 80)
    new_im = Image.new("RGB", new_size)
    box = tuple((n - o) // 2 for n, o in zip(new_size, old_size))
    new_im.paste(old_im, box)
    new_im.save(enlarged_filename)

    # We remove the background of the new large image
    without_background_filename = create_temp_filename('without_background.png')
    remove_image_background(enlarged_filename, without_background_filename)

    img = __read_image(without_background_filename)
    alpha = __extract_alpha_channel(img)
    big_contour = __get_largest_contour(alpha)
    contour_img = __draw_filled_contour_on_black_background(big_contour, alpha.shape)
    dilate = __apply_dilation(contour_img)
    canvas = np.zeros(img.shape, dtype = np.uint8)
    canvas = __apply_overlays(canvas, img, dilate)
    # The image is as larg as the original, maybe we need to crop it
    large_result_filename = create_temp_filename('large.png')
    Image.fromarray(canvas.astype(np.uint8), mode = 'RGBA').save(large_result_filename)
    # Cropping considering non-alpha pixels as dimension to preserve
    im = cv2.imread(large_result_filename, cv2.IMREAD_UNCHANGED)
    x, y, w, h = cv2.boundingRect(im[..., 3])
    im2 = canvas[y:y+h, x:x+w, :]
    
    if output_filename: 
        cv2.imwrite(output_filename, cv2.cvtColor(im2, cv2.COLOR_RGBA2BGRA))
    else:
        return canvas.astype(np.uint8)

def __read_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

def __extract_alpha_channel(img):
    return img[:, :, 3]

def __get_largest_contour(alpha_channel):
    # Smoothing using GaussianBlur
    smoothed = cv2.GaussianBlur(alpha_channel, (15, 15), 0)
    contours_smoothed = cv2.findContours(smoothed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_smoothed = contours_smoothed[0] if len(contours_smoothed) == 2 else contours_smoothed[1]
    big_contour_smoothed = max(contours_smoothed, key = cv2.contourArea)

    # Use the smoothed contour
    peri = cv2.arcLength(big_contour_smoothed, True)
    return cv2.approxPolyDP(big_contour_smoothed, 0.001 * peri, True)

def __draw_filled_contour_on_black_background(big_contour, shape):
    contour_img = np.zeros(shape)
    cv2.drawContours(contour_img, [big_contour], 0, 255, -1)
    return contour_img

def __apply_dilation(img):
    # TODO: This is missing in source (https://withoutbg.com/resources/creating-sticker)
    # (5, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

def __apply_overlays(canvas, img, dilate):
    alpha = np.expand_dims(img[:, :, 3], 2)
    alpha = np.repeat(alpha, 3, 2)
    alpha = alpha / 255

    canvas[dilate == 255] = (255, 255, 255, 255)
    canvas[:, :, 0:3] = canvas[:, :, 0:3] * (1 - alpha) + alpha * img[:, :, 0:3]

    return canvas