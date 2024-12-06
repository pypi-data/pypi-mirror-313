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


LAPTOP_ON_TABLE_VIDEO_GREENSCREEN = GreenscreenDetails(
    greenscreen_areas = [
        GreenscreenAreaDetails(
            rgb_color = (0, 174, 62),
            similar_greens = [],
            upper_left_pixel = (569, 229),
            lower_right_pixel = (1385, 737),
            frames = None
        )
    ],
    filename_or_google_drive_url = 'https://drive.google.com/file/d/1_luaJcNqP49AzeXuF4LPpAq7LvNzr95O/view?usp=sharing',
    type = GreenscreenType.VIDEO
)