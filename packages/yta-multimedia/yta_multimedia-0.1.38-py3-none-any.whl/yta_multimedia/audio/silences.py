from yta_multimedia.audio.parser import AudioParser
from yta_general_utils.programming.parameter_validator import NumberValidator
from pydub import silence


class AudioSilence:
    """
    Class to simplify and encapsulate the interaction with audio silences.
    """
    @staticmethod
    def detect(audio, minimum_silence_ms: int):
        """
        Detect the silences of a minimum of 'minimum_silence_ms' milliseconds
        time and returns an array containing tuples with the start and the 
        end of the silence moments.
        """
        audio = AudioParser.to_audiosegment(audio)

        if not minimum_silence_ms:
            minimum_silence_ms = 250

        if not NumberValidator.is_positive_number(minimum_silence_ms):
            raise Exception('The provided "minimum_silence_ms" is not a positive number.')

        dBFS = audio.dBFS
        # TODO: Why '- 16' (?) I don't know
        silences = silence.detect_silence(audio, min_silence_len = minimum_silence_ms, silence_thresh = dBFS - 16)

        # [(1.531, 1.946), (..., ...), ...] in seconds
        return [((start / 1000), (stop / 1000)) for start, stop in silences]