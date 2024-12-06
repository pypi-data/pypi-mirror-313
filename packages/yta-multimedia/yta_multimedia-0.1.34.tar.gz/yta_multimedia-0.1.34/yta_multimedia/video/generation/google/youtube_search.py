from yta_multimedia.video.utils import generate_video_from_image
from yta_multimedia.resources.image.drive_urls import YOUTUBE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.audio.sound.generation.sound_generator import SoundGenerator
from yta_multimedia.resources import Resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from moviepy import TextClip, CompositeVideoClip


# TODO: This is too repetitive with the same videos around the search
# please, make it dynamic, maybe with scrapper and saving frames
class YoutubeSearch():
    def generate(self, text: str):
        _EXTENDED_DURATION = 0.5
        _DURATION = 3

        # Download the resource we need
        TMP_FILENAME = Resource.get(YOUTUBE_SEARCH_IMAGE_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'images/youtube_search.png')
        clip = clip = generate_video_from_image(TMP_FILENAME, _DURATION + _EXTENDED_DURATION)

        # Calculate each char duration and set texts according to this
        text_len = len(text)
        each_char_duration = _DURATION / text_len

        clips = []
        for i in range(text_len):
            # Generate a text clip for each text writing part
            txt_clip = TextClip(text[:i + 1], font = 'Arial', fontsize = 25, color = 'black')
            clip_duration = each_char_duration
            
            if i == (text_len - 1):
                clip_duration = each_char_duration + _EXTENDED_DURATION
            
            txt_clip = txt_clip.with_position([540, 37]).with_duration(clip_duration).with_start(i * each_char_duration)

            clips.append(txt_clip)

        video = CompositeVideoClip([clip] + clips)
        # Here we have the text being written, we need the sound
        audio = SoundGenerator.create_typing_audio()
        video = video.with_audio(audio)

        return video