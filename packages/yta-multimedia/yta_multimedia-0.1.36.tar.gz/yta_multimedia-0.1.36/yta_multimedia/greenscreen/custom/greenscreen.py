from yta_multimedia.greenscreen.custom.image_greenscreen import ImageGreenscreen
from yta_multimedia.greenscreen.custom.video_greenscreen import VideoGreenscreen
from yta_multimedia.resources import Resource
from yta_multimedia.greenscreen.utils import GREENSCREENS_FOLDER
from yta_general_utils.checker.url import url_is_ok
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.checker.url import is_google_drive_url
from yta_general_utils.downloader.google_drive import GoogleDriveResource


class Greenscreen:
    """
    This class is an initializer of the ImageGreenscreen and 
    VideoGreenscreen classes so you provide the valid filename
    or Google Drive url of a greenscreen to the 'init' method
    and you get the corresponding ImageGreenscreen or 
    VideoGreenscreen initialized and ready to work.

    If you provide a Google Drive url the system will identify
    the resource and download it only if necessary, as it will
    create locally a unique identifier with the Google Drive ID
    so once it's been downloaded the first time it will be get
    from the local source the next time.

    This will not be possible if a local path is given as the
    system will not be able to identify the resource and the
    greenscreen processing time will be long in any execution.
    """
    @classmethod
    def init(cls, filename_or_google_drive_url: str):
        """
        Parses the provided parameter 'filename_or_google_drive_url' and
        checks if it is a valid filename or a valid Google Drive url. If
        valid, it dowloads the resource (if necessary) and checks if the
        file is an image or a video and returns the corresponding
        ImageGreenscreen or VideoGreenscreen.

        This method will raise an Exception if something goes wrong.
        """
        is_a_file = FileValidator.is_file(filename_or_google_drive_url)
        is_url = False
        filename = filename_or_google_drive_url

        if not is_a_file:
            is_url = url_is_ok(filename_or_google_drive_url)

            if not is_url:
                raise Exception(f'The provided greenscreen "{filename_or_google_drive_url}" parameter is not a file nor a valid url.')
            
            if not is_google_drive_url(filename_or_google_drive_url):
                raise Exception(f'The provided greenscreen "url" parameter "{filename_or_google_drive_url}" is not a valid Google Drive url.')
            
            google_drive_id = GoogleDriveResource(filename_or_google_drive_url).id
            folder = GREENSCREENS_FOLDER + google_drive_id + '/'
            # Extension will be replaced with real one
            filename = Resource.get(filename_or_google_drive_url, folder + 'greenscreen.png')

        # We have a valid filename, lets check if video or image
        if FileValidator.file_is_image_file(filename):
            return ImageGreenscreen(filename)
        elif FileValidator.file_is_video_file(filename):
            return VideoGreenscreen(filename)
        else:
            raise Exception(f'The greenscreen file "{filename}" is not a valid image or video file.')
    