from moviepy import AudioFileClip, concatenate_audioclips
from yta_multimedia.resources.audio.drive_urls import TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL, SILENCE_10_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from yta_multimedia.resources import Resource
from typing import Union


class SoundGenerator:
    # TODO: Move this to a consts.py file
    SILENCE_SOUND_FILENAME = EFFECTS_RESOURCES_FOLDER + 'sounds/silence_10s.mp3'
    TYPING_SOUND_FILENAME = EFFECTS_RESOURCES_FOLDER + 'sounds/typing_keyboard_3s.mp3'

    @classmethod
    def create_silence_audio(cls, duration: float, output_filename: Union[str, None] = None):
        """
        Creates a silence audioclip of the provided 'duration'. If
        'output_filename' is provided, it is also stored locally 
        with that name.
        """
        # TODO: Generate the silence without files but with
        # AudioSegment or another library
        if not duration:
            raise Exception('No "duration" provided.')
        
        silence_audioclip = AudioFileClip(Resource.get(SILENCE_10_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL, cls.SILENCE_SOUND_FILENAME))
        audioclip = silence_audioclip.copy()

        # Duration is 10s, so if we need more time we need to concatenate it
        times_to_concat = int(duration // silence_audioclip.duration)
        for _ in range(times_to_concat):
            audioclip = concatenate_audioclips([audioclip, silence_audioclip])

        audioclip = audioclip.with_subclip(0, duration)

        if output_filename:
            audioclip.write_audiofile(output_filename)

        return audioclip

    @classmethod
    def create_typing_audio(cls, output_filename: Union[str, None] = None):
        """
        Creates a typing audioclip of 3.5 seconds that, if 
        'output_filename' is provided, is stored locally
        with that name.
        """
        audio_filename = Resource.get(TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL, cls.TYPING_SOUND_FILENAME)
        audioclip = AudioFileClip(audio_filename)
        silence_audioclip = cls.create_silence_audio(0.5)

        audioclip = concatenate_audioclips([audioclip, silence_audioclip])

        if output_filename:
            audioclip.write_audiofile(output_filename)

        return audioclip
