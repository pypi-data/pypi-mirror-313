from yta_multimedia.video.frames.numpy_frame_helper import NumpyFrameHelper, FrameMaskingMethod

import numpy as np


class VideoFrame:
    """
    Class to represent a video frame, to simplify the way
    we turn it into a mask and work with it. A mask frame
    is a numpy array with single values per pixel and 
    values between 0.0 and 1.0 (where 0.0 is full 
    full transparent and 1.0 is full opaque). A normal
    frame is a numpy array with 3 values per pixels
    (representing R, G, B) and values between 0 and 255 
    (where 0 is the absence of color and 255 the full
    presence of that color).

    This class has been created to work easily with frames
    and to verify them when creating a new instance.
    """
    frame: np.ndarray = None
    """
    The frame information as a numpy array. This array can
    only contain frames in the format of not normalized
    RGB (array of 3 values from 0 to 255 per pixel) or
    normalized alpha (1 single value per pixel from 0.0 to
    1.0).
    """
    _is_mask: bool = None

    @property
    def is_mask(self):
        """
        Return True if the stored 'frame' is a mask, which means
        that it is a numpy array of single values between 0.0 and
        1.0 (representing the opacity, which 0.0 as full
        transparent and 1.0 as full opaque).
        """
        return self._is_mask
    
    @property
    def is_normal(self):
        """
        Return True if the stored 'frame' is a normal frame, which
        means that it is a numpy array of 3 values (R, G, B) between
        0 and 255 (representing the color presence, with 0 as no
        color and 255 as full color).
        """
        return self._is_mask == False

    def __init__(self, frame: np.ndarray):
        if not NumpyFrameHelper.is_rgb_not_normalized(frame) and not NumpyFrameHelper.is_rgb_normalized(frame) and not NumpyFrameHelper.is_alpha_normalized(frame) and not NumpyFrameHelper.is_alpha_not_normalized(frame):
            # TODO: Print properties to know why it is not valid
            raise Exception('The provided "frame" is not a valid frame.')

        is_mask = False
        if NumpyFrameHelper.is_alpha(frame):
            is_mask = True
            # We ensure it is a normalized alpha frame to store it
            frame = NumpyFrameHelper.as_alpha(frame)
        elif NumpyFrameHelper.is_rgb(frame):
            # We ensure it is a not normalized normal frame to store it
            frame = NumpyFrameHelper.as_rgb(frame)
        else:
            raise Exception('The provided "frame" is not an alpha nor a rgb frame.')

        self.frame = frame
        self._is_mask = is_mask

    def as_mask(self, masking_method: FrameMaskingMethod = FrameMaskingMethod.MEAN):
        """
        Return the frame as a mask by applying the 'masking_method'
        if necessary.
        """
        if self.is_mask:
            return self.frame
        
        return NumpyFrameHelper.as_alpha(self.frame, do_normalize = True, masking_method = masking_method)
    
    def inverted(self):
        """
        Return the frame inverted. This method does not modify
        the object itself.
        """
        return NumpyFrameHelper.invert(self.frame)
    
    def normalized(self):
        """
        Return the frame normalized (with values between 0.0
        and 1.0). This method does not modify the object
        itself.
        """
        return NumpyFrameHelper.normalize(self.frame)

    def denormalized(self):
        """
        Return the frame denormalized (with values between 0
        and 255). This method does not modify the object
        itself.
        """
        return NumpyFrameHelper.denormalize(self.frame)

