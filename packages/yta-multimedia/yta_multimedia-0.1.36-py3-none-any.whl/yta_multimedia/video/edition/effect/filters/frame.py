from skimage.filters import gaussian as skimage_gaussian
from typing import Union


class FrameFilter:
    """
    Filters to be applied on moviepy video frames so we
    can modify them by using 'clip.transform' method.

    Example below:
    ``` 
    clip.transform(
        lambda get_frame, t:
        FrameFilter.blur(get_frame, t, blur_radius = blur_radius)
    )
    ```
    
    """
    @staticmethod
    def blur(get_frame, t, blur_radius: Union[int, None] = None):
        return skimage_gaussian(get_frame(t).astype(float), sigma = blur_radius)