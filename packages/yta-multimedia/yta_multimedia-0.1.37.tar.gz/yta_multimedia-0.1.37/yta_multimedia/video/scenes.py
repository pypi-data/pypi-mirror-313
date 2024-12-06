from yta_multimedia.video.parser import VideoParser
from moviepy.Clip import Clip
from scenedetect import SceneManager, open_video, ContentDetector


def detect_scenes_from_video(video: Clip):
    """
    This method detects the different scenes that are in the provided 'video_input'
    video file and returns an array containing 'start' and 'end' elements. Each of 
    those contains a 'second' and 'frame' field.

    TODO: This link https://www.scenedetect.com/docs/latest/api.html#example says that
    there is a backend 'VideoStreamMoviePy' class to process it with moviepy. This is
    interesting to use in a clip, and not in a filename.
    """
    # This comes from here: https://www.scenedetect.com/
    # Other project: https://github.com/slhck/scenecut-extractor (only ffmpeg)
    video = VideoParser.to_moviepy(video)
    # TODO: I think this has to be a path so it is not able to
    # detect scenes from a video in memory (?)

    # TODO: Check if thiss 'filename' includes the abspath
    video = open_video(video.filename, backend = 'moviepy')
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold = 20))  # 27 is recommended
    scene_manager.detect_scenes(video)

    scenes = []
    for scene in scene_manager.get_scene_list():
        scenes.append({
            'start': {
                'second': scene[0].get_seconds(),
                'frame': scene[0].get_frames()
            },
            'end': {
                'second': scene[1].get_seconds(),
                'frame': scene[1].get_frames()
            }
        })

    return scenes

    # This code below is working but it is quite old
    
    from scenedetect import VideoManager, SceneManager, StatsManager
    from scenedetect.detectors import ContentDetector
    from scenedetect.scene_manager import save_images, write_scene_list_html

    video_manager = VideoManager([video_filename])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    scene_manager.add_detector(ContentDetector(threshold = 30))
    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source = video_manager)

    scenes = scene_manager.get_scene_list()
    print(f'{len(scenes)} scenes detected!')

    save_images(
        scenes,
        video_manager,
        num_images = 1,
        image_name_template = '$SCENE_NUMBER',
        output_dir = 'scenes')

    for scene in scenes:
        start, end = scene

        # your code
        print(f'{start.get_seconds()} - {end.get_seconds()}')

    return scenes


# This is to work with abruptness and sooness (https://moviepy.readthedocs.io/en/latest/ref/videofx/moviepy.video.fx.all.accel_decel.html)
    
# I previously had 4.4.2 decorator for moviepy. I forced 4.0.2 and it is apparently working

"""
Interesting:
- https://www.youtube.com/watch?v=Ex1kuxe6jRg (el canal entero tiene buena pinta)
- https://www.youtube.com/watch?v=m6chqKlhpPo Echarle un vistazo a ese tutorial
- https://zulko.github.io/moviepy/ref/videofx.html
- https://stackoverflow.com/questions/48491070/how-to-flip-an-mp4-video-horizontally-in-python
"""
