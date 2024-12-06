from yta_multimedia.greenscreen.utils import get_greenscreen_areas_details
from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_multimedia.greenscreen.classes.greenscreen_area_details import GreenscreenAreaDetails
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.greenscreen.enums import GreenscreenType
from yta_multimedia.greenscreen.utils import GREENSCREENS_FOLDER
from yta_multimedia.resources import Resource
from yta_general_utils.downloader.google_drive import GoogleDriveResource
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.checker.url import is_google_drive_url


def get_greenscreen_details(greenscreen_filename_or_google_drive_url: str, type: GreenscreenType):
    """
    Method to obtain greenscreen area and details that must be
    used by ImageGreenscreen and VideoGreenscreen to automatically
    detect greenscreens in their resources.
    """
    if not greenscreen_filename_or_google_drive_url:
        return None
    
    # TODO: Check that 'type' is GreenscreenType type

    # We will need the resource filename or google drive url and
    # the image to extract the data from
    RESOURCE_FILENAME = greenscreen_filename_or_google_drive_url
    TMP_FILENAME = greenscreen_filename_or_google_drive_url

    if type == GreenscreenType.IMAGE:
        # We have the final resource and the image to extract data
        if is_google_drive_url(greenscreen_filename_or_google_drive_url):
            google_drive_id = GoogleDriveResource(greenscreen_filename_or_google_drive_url).id
            filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.png'
            TMP_FILENAME = Resource.get(greenscreen_filename_or_google_drive_url, filename)
    elif type == GreenscreenType.VIDEO:
        if is_google_drive_url(greenscreen_filename_or_google_drive_url):
            google_drive_id = GoogleDriveResource(greenscreen_filename_or_google_drive_url).id
            filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4'
            RESOURCE_FILENAME = Resource.get(greenscreen_filename_or_google_drive_url, filename)
        TMP_FILENAME = create_temp_filename('tmp_gs_autodetect.png')
        VideoFrameExtractor.get_frame_by_number(RESOURCE_FILENAME, 0, TMP_FILENAME)
    else:
        raise Exception(f'The greenscreen type "{type}" is not a valid image or video file.')

    green_rgb_color, similar_greens, regions = get_greenscreen_areas_details(TMP_FILENAME)

    if not green_rgb_color:
        raise Exception('No automatic greenscreen detected in "' + greenscreen_filename_or_google_drive_url + '". Aborting.')

    greenscreen_areas = []
    for region in regions:
        greenscreen_areas.append(GreenscreenAreaDetails(
            rgb_color = green_rgb_color,
            similar_greens = similar_greens,
            # TODO: Rename this (?)
            upper_left_pixel = region.top_left,
            lower_right_pixel = region.bottom_right,
            frames = None # TODO: Implement a way of handling frames
        ))

    greenscreen_filename_or_google_drive_url = GreenscreenDetails(
        greenscreen_areas = greenscreen_areas,
        filename_or_google_drive_url = RESOURCE_FILENAME,
        type = type
    )

    return greenscreen_filename_or_google_drive_url