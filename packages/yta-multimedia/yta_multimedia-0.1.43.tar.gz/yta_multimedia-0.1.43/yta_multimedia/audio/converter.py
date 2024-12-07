from yta_multimedia.audio.parser import AudioParser
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.file.filename import ensure_file_extension
from yta_general_utils.programming.enum import YTAEnum as Enum


class AudioExtension(Enum):
    """
    Enum class to encapsulate the accepted audio extensions for our
    system.
    """
    # TODO: Maybe interconnect with 'ffmpeg_handler.py' Enums
    MP3 = 'mp3'
    WAV = 'wav'
    M4A = 'm4a'
    WMA = 'wma'
    CD = 'cd'
    OGG = 'ogg'
    AIF = 'aif'
    # TODO: Check which extensions are valid for the AudioSegment
    # and the 'export' method to be able to classify AudioExtension
    # enums in AudioSegmentAudioExtension or similar because we
    # should also have AudioExtension for the FfmpegHandler...

class AudioConverter:
    """
    Class to simplify and encapsulate the functionality related to
    audio conversion.
    """
    @staticmethod
    def to(audio, extension: AudioExtension, output_filename: str):
        """
        This method converts the provided 'audio' to a audio with
        the provided 'extension' by storing it locally as the 
        provided 'output_filename' (or as a temporary file if not
        provided), and returns the new audio and the filename.

        This method returns two values: audio, filename
        """
        audio = AudioParser.to_audiosegment(audio)
        extension = AudioExtension.to_enum(audio)

        if not output_filename:
            # TODO: Replace this when not exporting needed
            output_filename = create_temp_filename(f'tmp_converted_sound.{extension.value}')
        else:
            output_filename = ensure_file_extension(output_filename, extension.value)

        audio.export(output_filename, format = extension.value)
        audio = AudioParser.to_audiosegment(output_filename)

        return audio, output_filename

    @staticmethod
    def to_wav(audio, output_filename: str):
        """
        This method converts the provided 'audio' to a wav audio
        by storing it locally as the provided 'output_filename'
        (or as a temporary file if not provided), and returns the
        new audio and the filename.

        This method returns two values: audio, filename
        """
        return AudioConverter.to(audio, AudioExtension.WAV, output_filename)
    
    @staticmethod
    def to_mp3(audio, output_filename: str):
        """
        This method converts the provided 'audio' to a mp3 audio
        by storing it locally as the provided 'output_filename'
        (or as a temporary file if not provided), and returns the
        new audio and the filename.

        This method returns two values: audio, filename
        """
        return AudioConverter.to(audio, AudioExtension.MP3, output_filename)