"""
    In this file we register all video greenscreens we have
    available in our system. These greenscreens have their
    own resource uploaded to Google Drive and we have also
    detected the greenscreen color and the pixels in which
    the area is and we define those parameters below.

    This file is for letting these greenscreens to be used
    by the VideoGreenscreen class to inject some pictures
    or videos on it and enhance the video experience.

    TODO: Read below
    This should be replaced by a database in which we store
    this information and keep it updated, not directly in
    code, but for now it is our system.
"""
from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_multimedia.greenscreen.classes.greenscreen_area_details import GreenscreenAreaDetails
from yta_multimedia.greenscreen.enums import GreenscreenType


YOUTUBE_VIDEO_IMAGE_GREENSCREEN = GreenscreenDetails(
    greenscreen_areas = [
        GreenscreenAreaDetails(
            rgb_color = (0, 249, 12),
            similar_greens = [],
            upper_left_pixel = (28, 110),
            lower_right_pixel = (1282, 817),
            frames = None
        )
    ],
    filename_or_google_drive_url = 'https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=sharing',
    type = GreenscreenType.IMAGE
)

NOT_ONLY_ONE_IMAGE_GREENSCREEN = GreenscreenDetails(
    greenscreen_areas = [
        GreenscreenAreaDetails(
            rgb_color = (75, 239, 20),
            similar_greens = [],
            upper_left_pixel = (200, 502),
            lower_right_pixel = (775, 825),
            frames = None
        ),
        GreenscreenAreaDetails(
            rgb_color = (75, 239, 20),
            similar_greens = [],
            upper_left_pixel = (1098, 132),
            lower_right_pixel = (1673, 445),
            frames = None
        )
    ],
    filename_or_google_drive_url = 'C:/Users/dania/Desktop/doublegs1080.png',
    type = GreenscreenType.IMAGE
)