from yta_multimedia.resources import Resource
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.image.region.image_region_finder import ImageRegionFinder
from yta_general_utils.file.reader import FileReader
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.path import create_file_abspath
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.downloader.google_drive import GoogleDriveResource
from yta_general_utils.image.color.picker import ColorPicker
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.image.converter import ImageConverter
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx import MaskColor
from typing import Union, Any


# TODO: Review all this code please, a lot is duplicated
# TODO: Make this below expect a type 'Image', but 'Image' or
# 'Image.Image' returns each arg must be a type. Got <module 
# 'PIL.Image'. We also can expect np.ndarray when read from
# memory (video.get_frame(...))
def get_greenscreen_areas_details(image: Union[str, Any]):
    """
    This method detects the most common green rgb color and
    the different closed regions in the provided 'image'. The
    'image' must be a filename or a Pillow image instance.

    This method returns a sequence of the 3 found elements:
    the most common green rgb color, the similar green colors
    and the regions found.
    """
    # TODO: Improve the way we check np.ndarray information so
    # we can make sure it is a valid image and not any other
    # kind of information

    # Sometimes it comes from a moviepy clip turned into np
    image = ImageParser.to_pillow(image)
    
    green_rgb_color, similar_greens = ColorPicker.get_most_common_green_rgb_color_and_similars(image)
    regions = ImageRegionFinder.find_green_regions(ImageConverter.pil_image_to_numpy(image))

    return green_rgb_color, similar_greens, regions


"""
        Moving Greenscreens below
        TODO: Move this below to another more specific file, thank you
        TODO: I'm placing this below here by now, but maybe we should
        build a 'MovingVideoGreenscreen' object for this
"""

# TODO: Move this to a consts.py or something
GREENSCREENS_FOLDER = 'resources/greenscreens/'

def insert_video_into_moving_greescreen(greenscreen_google_drive_url: str, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, str], output_filename: Union[str, None] = None):
    """
    This method inserts the provided 'video' into the moving greenscreen
    that is contained in the provided 'greenscreen_google_drive_url'. It
    will extract all greenscreen frames, analyze each of them and extract
    the greenscreen areas information and put the provided 'video' 
    combined with the greenscreen.

    This method will identify the Google Drive ID to store (or load if
    previously downloaded) the moving greenscreen video to be able to
    handle it. It will use one specific folder to work with the data:
    'resources/greenscreens/GOOGLE_DRIVE_ID', extracting
    the frames, generating a 'config.json' file and also downloading
    the resource from Google Drive.

    @param
        **greenscreen_google_drive_url**
        The Google Drive url of the moving greenscreen video resource.

    @param
        **video**
        The filename of the video we want to put into the greenscreen.

    @param
        **output_filename**
        The filename in which we want to write the final video that is
        our 'video' inside of the greenscreen.
    """
    video = VideoParser.to_moviepy(video)
    
    __preprocess_moving_greenscreen(greenscreen_google_drive_url)

    # Here we have the moving greenscreen with the source file and
    # the config file ready to use
    google_drive_id = GoogleDriveResource(greenscreen_google_drive_url).id
    moving_gs_folder = GREENSCREENS_FOLDER + google_drive_id
    greenscreen_filename = moving_gs_folder + '/greenscreen.mp4'
    greenscreen_config_filename = moving_gs_folder + '/config.json'

    moving_gs = VideoFileClip(greenscreen_filename)

    if moving_gs.duration < video.duration:
        video = video.with_duration(moving_gs.duration)
    elif video.duration < moving_gs.duration:
        moving_gs = moving_gs.with_duration(video.duration)

    # We dynamically load main video frames
    frames = VideoFrameExtractor.get_all_frames(video)

    greenscreen_details = FileReader.read_json_from_file(greenscreen_config_filename)

    # Now lets put together greenscreen and main video frames
    # applying a mask to build the final video by concatenating
    # them
    final_clips = []
    for index, frame in enumerate(frames):
        frame_details = greenscreen_details[str(index)]

        # We need to put the image into the greenscreen frame
        imageclip = ImageClip(frame, duration = 1 / 60)
        
        # TODO: Pay atenttion to this:
        # I have a 'to_video' method in ImageGreenscreen that
        # should be used here, but I can't. Why? Because of its 
        # behaviour right now. ImageGreenscreen object is not
        # prepared to have numpy images stored to be used later,
        # so when I call the 'to_video' method I should be able
        # to use the frame I get here below, but I can't because
        # it is expecting an image on Google Drive or a local
        # storaged filename. I don't want to write the frame
        # because of performance decreases, so I leave this text
        # here for the future, to make own custom Greenscreen
        # objects able to handle images and videos loaded in
        # memory to work with.

        # Inject the imageclip
        # TODO: This is a sensitive part, documentation says something
        # about masks when numpy provided, but this is working
        green_screen_clip = ImageClip(VideoFrameExtractor.get_frame_by_number(moving_gs, index), duration = imageclip.duration).with_effects([MaskColor(color = frame_details['rgb_color'], threshold = 100, stiffness = 5)])
        
        # We cannot resize with numpys
        imageclip = imageclip.resized(width = frame_details['lower_right_pixel'][0] - frame_details['upper_left_pixel'][0]).with_position((frame_details['upper_left_pixel'][0], frame_details['upper_left_pixel'][1]))

        final_clips.append(CompositeVideoClip([imageclip, green_screen_clip], size = green_screen_clip.size))

    final = concatenate_videoclips(final_clips).with_audio(video.audio)

    if output_filename:
        final.write_videofile(output_filename, fps = video.fps)

    return final

def __prepare_moving_greenscreen(google_drive_url: str):
    """
    This method will download (if needed) the resource from Google
    Drive to local and will create (if it doesn't exist) the config
    file of a moving Greenscreen.

    TODO: What about other greenscreens (?)

    @param
        **google_drive_url**
        The Google Drive url of the greenscreen. This will be used
        to download the source file and also to identify it with
        the Google Drive ID.
    """
    if not google_drive_url:
        raise Exception('No "google_drive_url" provided.')

    # The identifier of the greenscreen is the Google Drive id
    google_drive_id = GoogleDriveResource(google_drive_url).id
    greenscreen_filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4'
    config_filename = GREENSCREENS_FOLDER + google_drive_id + '/config.json'

    # Check if folder exist or not, and create it if not
    create_file_abspath(get_project_abspath() + greenscreen_filename)

    # TODO: What about image Greenscreen, not .mp4 (?)

    # Check if video exist
    if not FileValidator.file_exists(greenscreen_filename):
        Resource.get(google_drive_url, GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4')

    # Check if config file exist
    if not FileValidator.file_exists(config_filename):
        FileWriter.write_json_to_file({}, config_filename)

def __preprocess_moving_greenscreen(greenscreen_google_drive_url: str):
    """
    This method analyzes, frame by frame, a video greenscreen and stores
    each frame information about greenscreen area in a config file to
    be lately used for video injection.
    """
    if not greenscreen_google_drive_url:
        raise Exception('No "greenscreen_google_drive_url" provided.')
    
    # First, make sure config file and source file are available
    __prepare_moving_greenscreen(greenscreen_google_drive_url)

    google_drive_id = GoogleDriveResource(greenscreen_google_drive_url).id
    filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4'

    # Read the video and extract frames
    gs_clip = VideoFileClip(filename)

    for i in range((int) (gs_clip.fps * gs_clip.duration)):
        __process_moving_greenscreen_frame(greenscreen_google_drive_url, i)

    return

def __process_moving_greenscreen_frame(greenscreen_google_drive_url: str, frame_number: int, do_force: bool = False):
    """
    This method processes the 'frame_number' frame of the existing
    greenscreen in 'greenscreen_google_drive_url' source. It will
    detect the greenscreen area of that frame and store it in the
    specific configuration file.

    This method will store the information in an specific folder
    'resources/greenscreens/frames/GOOGLE_DRIVE_ID/'. All
    the information is the greenscreen video, the frames and the
    'config.json' file that contains the detailed greenscreen
    areas of each frame. As you can see, the 'GOOGLE_DRIVE_ID' is
    used as identifier.

    If that 'frame_number' has been previously analyzed, the 
    system will do it again only if the 'do_force' parameter
    is True. If not, it will stop and return.

    @param
        **greenscreen_google_drive_url**
        The Google Drive url that contains the greenscreen video
        from which we will analyze the frame.
    
    @param
        **frame_number**
        The frame number that will be analyzed. The first frame of
        the greenscreen is the number 0.

    @param
        **do_force**
        The information of that 'frame_number' could be stored 
        previously so it would be ignored. You can set this
        parameter to True to force recalculating the frame.
    """
    if not greenscreen_google_drive_url:
        return None
    
    if frame_number < 0:
        return None
    
    # We always make sure greenscreen source file and config are ready
    __prepare_moving_greenscreen(greenscreen_google_drive_url)

    # sample url: https://drive.google.com/file/d/1My5V8gKcXDQGGKB9ARAsuP9MIJm0DQOK/view?usp=sharing
    google_drive_id = GoogleDriveResource(greenscreen_google_drive_url).id
    
    config_filename = GREENSCREENS_FOLDER + google_drive_id + '/config.json'
    greenscreen_filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4'

    json_data = FileReader.read_json_from_file(config_filename)

    if str(frame_number) in json_data and not do_force:
        # Frame information found and no forcing
        return

    # We make sure we have the clip (and resource)
    gs_clip = VideoFileClip(greenscreen_filename)

    greenscreen_frames_number = (int) (gs_clip.fps * gs_clip.duration)
    if frame_number > (greenscreen_frames_number):
        raise Exception('The requested "frame_number" is not valid. The greenscreen only has "' + str(greenscreen_frames_number) + '" frames.')
    
    # This below stores the frame and use it later for analysis (working)
    # output_filename = create_temp_filename('tmp_frame.png')
    # get_frame_from_video_by_frame_number(gs_clip, frame_number, output_filename)
    # details = get_greenscreen_areas_details(output_filename)

    # This below tries to do with numpy
    # TODO: Maybe this is making it slow (too much memory)
    green_rgb_color, similar_greens, green_regions = get_greenscreen_areas_details(VideoFrameExtractor.get_frame_by_number(gs_clip, frame_number))

    json_data[frame_number] = {
        'index': frame_number,
        'rgb_color': green_rgb_color,
        'similar_greens': similar_greens,
        # TODO: I keep doing this to break not the functionality but
        # we need to be able to handle different green areas now that
        # we are able to do it
        'upper_left_pixel': green_regions[0]['top_left'],
        'lower_right_pixel': green_regions[0]['bottom_right'],
        'frames': None
    }

    return FileWriter.write_json_to_file(json_data, config_filename)