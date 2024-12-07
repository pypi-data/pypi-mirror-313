from yta_multimedia.video.transition.objects import TransitionMode, TransitionMethod, VideoTransition, Transition
from yta_multimedia.video.position import Position
from moviepy.Clip import Clip


class AlphaTransition(Transition):
    """
    Transition between 2 videos that is made by applying
    an alpha video as a mask to make the first video
    transition to the second one.

    The alpha video must be, if possible, a pure black and
    white video (transparency is accepted) that goes from
    black to white, as black color will be opaque and white
    will be transparent letting the second video appear.
    """
    def __init__(self, video1: Clip, video2: Clip, mode: TransitionMode, duration: float, alpha_video: Clip):
        super().__init__(
            video1,
            VideoTransition(mode, duration, TransitionMethod.alpha, alpha_video = alpha_video),
            video2
        )

class SlideLeftTransition(Transition):
    """
    Transition between 2 videos that is made by making
    the first video disappear from one side of the
    scene while the second video is appearing at the
    same time.
    """
    def __init__(self, video1: Clip, video2: Clip, mode: TransitionMode, duration: float):
        super().__init__(
            video1,
            VideoTransition(mode, duration, TransitionMethod.slide, side = Position.OUT_LEFT),
            video2
        )

class SlideRightTransition(Transition):
    """
    Transition between 2 videos that is made by making
    the first video disappear from one side of the
    scene while the second video is appearing at the
    same time.
    """
    def __init__(self, video1: Clip, video2: Clip, mode: TransitionMode, duration: float):
        super().__init__(
            video1,
            VideoTransition(mode, duration, TransitionMethod.slide, side = Position.OUT_RIGHT),
            video2
        )

class SlideTopTransition(Transition):
    """
    Transition between 2 videos that is made by making
    the first video disappear from one side of the
    scene while the second video is appearing at the
    same time.
    """
    def __init__(self, video1: Clip, video2: Clip, mode: TransitionMode, duration: float):
        super().__init__(
            video1,
            VideoTransition(mode, duration, TransitionMethod.slide, side = Position.OUT_TOP),
            video2
        )

class SlideBottomTransition(Transition):
    """
    Transition between 2 videos that is made by making
    the first video disappear from one side of the
    scene while the second video is appearing at the
    same time.
    """
    def __init__(self, video1: Clip, video2: Clip, mode: TransitionMode, duration: float):
        super().__init__(
            video1,
            VideoTransition(mode, duration, TransitionMethod.slide, side = Position.OUT_BOTTOM),
            video2
        )