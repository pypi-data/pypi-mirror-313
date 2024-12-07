from moviepy import AudioFileClip

import sox


def concatenate_audio_files(audio_filenames: list[str], output_filename: str):
    """
    Receives a set of audio filenames and turns them into a single file. This
    method writes the new file as 'output_filename' and returns the new file
    as an AudioFileClip.
    """
    if not output_filename:
        return None
    
    if not audio_filenames:
        return None
    # TODO: Check if all 'audio_filenames' provided are valid

    cbn = sox.Combiner()
    cbn.set_input_format(["mp3"] * len(audio_filenames), rate = [44100] * len(audio_filenames), channels = [2] * len(audio_filenames))
    cbn.convert(samplerate = 44100, n_channels = 2, bitdepth = 64)
    cbn.build(audio_filenames, output_filename, "concatenate")

    return AudioFileClip(output_filename)

def concatenate_audioclips(clips: list[AudioFileClip], output_filename: str):
    """
    Receives a set of AudioFileClips and turns them into a single file. This
    method writes the new file as 'output_filename' and returns the new file
    as an AudioFileClip.
    """
    if not output_filename:
        return None
    
    if not clips:
        return None
    # TODO: Check if all 'audio_filenames' provided are valid

    cbn = sox.Combiner()
    cbn.set_input_format(["mp3"] * len(clips), rate = [44100] * len(clips), channels = [2] * len(clips))
    cbn.convert(samplerate = 44100, n_channels = 2, bitdepth = 64)
    filenames = [clip.filename for clip in clips]
    cbn.build(filenames, output_filename, "concatenate")

    return AudioFileClip(output_filename)