"""
Mobject to represent a video inside of Manim. This video
Mobject is a modified ImageMobject that updates the 
content on each iteration.

This mobject is working properly with 'cairo' render and
using the 'ImageMobject' class for the inheritance.

TODO: Make this work with 'opengl' render by replacing 
the 'ImageMobject' with 'OpenGLImageMobject', but this
is returning a 'astype' exception when formating the
content with PIL lib in '.astype('uint8')'.

Thanks: https://gist.github.com/uwezi/faec101ed5d7c20222b33eee4b6c7d63
"""
from manim import *
from dataclasses import dataclass
from PIL import Image

import cv2


@dataclass
class VideoStatus:
    time: float = 0
    videoObject: cv2.VideoCapture = None

    def __deepcopy__(self, memo):
        return self

# TODO: Try to use 'OpenGLImageMobject' to be able
# to render in a 3D envinroment
# If trying with 'OpenGLImageMobject' you should
# use the 'opengl' animator , but this is failing
class VideoMobject(ImageMobject):
    '''
    Mobject that represents a video as a sequence of ImageMobjects
    that are updated as a video: frame by frame.

    This VideoMobject has been created to work with 'Cairo' render.
    It is working perfectly in 2D scenes and the video is also being
    displayed in 3D scenes but, in those cases, the positioning is
    being crazy, you cannot control the cameras.

    Parameters
    ----------
    filename
        the filename of the video file

    loop
        (optional) replay the video from the start in an endless loop

    https://discord.com/channels/581738731934056449/1126245755607339250/1126245755607339250
    2023-07-06 Uwe Zimmermann & Abulafia
    2024-03-09 Uwe Zimmermann
    '''
    def __init__(self, filename = None, loop = True, **kwargs):
        self.filename = filename
        self.speed = 1
        self.loop = loop
        self._id = id(self)
        self.status = VideoStatus()
        self.status.videoObject = cv2.VideoCapture(filename)

        self.status.videoObject.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, frame = self.status.videoObject.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            img = Image.fromarray(frame)
        else:
            img = Image.fromarray(np.uint8([[63, 0, 0, 0],
                                        [0, 127, 0, 0],
                                        [0, 0, 191, 0],
                                        [0, 0, 0, 255]
                                        ]))
        self.size = img.size

        super().__init__(img, **kwargs)

        if ret:
            self.add_updater(self.video_updater)

    def video_updater(self, mobj, dt):
        """
        This method updates the image (frame) that needs to be
        shown in the animation attending to the moment.
        """
        if dt == 0:
            return
        
        status = self.status
        status.time += 1000 * dt * mobj.speed
        self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
        ret, frame = self.status.videoObject.read()

        # Go to frame 0 if ended and loop requested
        if (ret == False) and self.loop:
            status.time = 0
            self.status.videoObject.set(cv2.CAP_PROP_POS_MSEC, status.time)
            ret, frame = self.status.videoObject.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # needed here?        
            img = Image.fromarray(frame)

            # Update the content (the image shown)
            mobj.pixel_array = change_to_rgba_array(
                np.asarray(img), mobj.pixel_array_dtype
            )

from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor

class VideoMobjectTest(ImageMobject):
    # TODO: Apply type to 'video'
    def __init__(self, video, **kwargs):
        # TODO: Check what video is
        # TODO: This is making the method fail (I don't know why)
        # if isinstance(video, str):
        #     video = VideoFileClip(video)

        self.frame_number = 0
        self.video = video
        self.filename = VideoFrameExtractor.get_frame_by_number(video, self.frame_number)

        super().__init__(self.filename, **kwargs)

        # We add the updater to update each frame
        self.add_updater(self.frame_by_frame_updater)

    def frame_by_frame_updater(self, mobj: Mobject, dt):
        self.frame_number += 1
        
        mobj.pixel_array = change_to_rgba_array(
            VideoFrameExtractor.get_frame_by_number(self.video, self.frame_number), mobj.pixel_array_dtype
        )