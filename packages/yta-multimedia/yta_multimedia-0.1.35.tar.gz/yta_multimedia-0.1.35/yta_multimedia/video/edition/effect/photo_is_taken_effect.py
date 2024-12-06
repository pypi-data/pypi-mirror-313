from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.blink_effect import BlinkEffect
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from yta_multimedia.resources.video.effect.sound.drive_urls import PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.resources import Resource
from moviepy import Clip, AudioFileClip, CompositeAudioClip


class PhotoIsTakenEffect(Effect):
    """
    Simulates that a photo is taken by making a white blink and
    a camera click sound. This effect doesn't freeze the video,
    it is just a white blink with a camera photo sound being
    played.

    This effect doesn't stop or freezes the video so it doesn't
    affect to its duration.

    What to do with the result? **REPLACE**

    The result should be replacing the original clip in the 
    affected part as it is still being reproduced while the
    effect is applied.
    """
    # TODO: Is this working (?)
    result_must_replace = True

    def apply(self, video: Clip) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        TMP_FILENAME = Resource.get(PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/photo_taken.mp3')

        # We force the effect to be last as much as the clip
        video = BlinkEffect().apply(video, [255, 255, 255])

        # TODO: Maybe raise an Exception as it is too short (?)
        effect_duration = video.duration if video.duration < effect_duration else 0.2

        video.audio = CompositeAudioClip([
            video.audio,
            AudioFileClip(TMP_FILENAME).with_duration(effect_duration)
        ])

        return video