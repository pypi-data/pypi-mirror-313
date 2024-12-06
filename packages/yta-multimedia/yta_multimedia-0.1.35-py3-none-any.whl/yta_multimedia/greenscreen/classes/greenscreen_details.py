from yta_multimedia.greenscreen.classes.greenscreen_area_details import GreenscreenAreaDetails
from yta_general_utils.downloader.google_drive import GoogleDriveResource
from yta_general_utils.checker.url import is_google_drive_url
from yta_multimedia.resources import Resource
from yta_multimedia.greenscreen.enums import GreenscreenType
from yta_multimedia.greenscreen.utils import GREENSCREENS_FOLDER
from typing import List


class GreenscreenDetails:
    """
    This class represents a greenscreen image or video
    resource, its information and the greenscreen areas
    that it contains.

    @param
        **greenscreen_areas**
        An array of _GreenscreenAreaDetails_ objects that
        represent the different greenscreen that there are
        inside this greenscreen resource.

    @param
        **filename_or_google_drive_url**
        The resource file filename or Google Drive url.
    """
    greenscreen_areas = []
    filename_or_google_drive_url = None
    type = None

    def __init__(self, greenscreen_areas: List[GreenscreenAreaDetails] = [], filename_or_google_drive_url: str = None, type: GreenscreenType = GreenscreenType.IMAGE):
        # TODO: Implement checkings please
        self.greenscreen_areas = greenscreen_areas
        self.filename_or_google_drive_url = filename_or_google_drive_url
        self.type = type

    def get_filename(self):
        """
        This method will return the video or image resource you need
        to use the greenscreen, that will be stored locally (and 
        maybe downloaded from Google Drive if it is not available
        in local storage yet).
        """
        # TODO: Change this behaviour and be more strict
        # and make more fields if needed, please
        filename = self.filename_or_google_drive_url

        if is_google_drive_url(self.filename_or_google_drive_url):
            google_drive_id = GoogleDriveResource(self.filename_or_google_drive_url).id
            folder = GREENSCREENS_FOLDER + google_drive_id + '/'

            filename = folder + 'greenscreen.mp4'
            if self.type == GreenscreenType.IMAGE:
                filename = folder + 'greenscreen.png'

            filename = Resource.get(self.filename_or_google_drive_url, filename)

        return filename