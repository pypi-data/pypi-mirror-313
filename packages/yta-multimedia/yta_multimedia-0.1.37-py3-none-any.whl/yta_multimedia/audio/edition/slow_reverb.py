from yta_multimedia.audio.converter import AudioConverter
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.temp import create_temp_filename
from math import trunc
from pedalboard import Pedalboard, Reverb

import numpy as np
import soundfile as sf


def slow_and_reverb_audio_file(audio_filename: str, output_filename: str, room_size: float = 0.75, damping: float = 0.5, wet_level: float = 0.08, dry_level: float = 0.2, delay: float = 2, slow_factor: float = 0.08):
    # Extracted from here: https://github.com/samarthshrivas/LoFi-Converter-GUI
    # But there is no only one: https://github.com/topics/slowedandreverbed
    if not audio_filename:
        return None
    
    if not FileValidator.file_is_audio_file(audio_filename):
        return None

    if not output_filename:
        return None
    
    if get_file_extension(audio_filename) != '.wav':
        # TODO: Handle other formats, by now I think it is .mp3 only
        tmp_filename = create_temp_filename('transformed_audio.wav')
        AudioConverter.to_wav(audio_filename, tmp_filename)
        audio_filename = tmp_filename

    audio, sample_rate = sf.read(audio_filename)
    sample_rate -= trunc(sample_rate * slow_factor)

    # Adding reverb effect
    reverved_board = Pedalboard([
        Reverb(
            # TODO: I need to learn more about these parameters
            room_size = room_size,
            damping = damping,
            wet_level = wet_level,
            dry_level = dry_level
        )
    ])

    # Adding other surrounding effects
    audio_with_effects = reverved_board(audio, sample_rate)
    channel_1 = audio_with_effects[:, 0]
    channel_2 = audio_with_effects[:, 1]
    shift_length = delay * 1000
    shifted_channel_1 = np.concatenate((np.zeros(shift_length), channel_1[:-shift_length]))
    combined_signal = np.hstack((shifted_channel_1.reshape(-1, 1), channel_2.reshape(-1, 1)))

    # Write the slowed and reverved output file
    sf.write(output_filename, combined_signal, sample_rate)

    return output_filename