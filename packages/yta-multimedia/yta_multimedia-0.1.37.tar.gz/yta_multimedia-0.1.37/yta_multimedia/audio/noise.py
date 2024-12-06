from yta_multimedia.audio.parser import AudioParser
from yta_multimedia.audio.converter import AudioConverter
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.file.remover import FileRemover
from df.enhance import enhance, init_df, load_audio, save_audio


class AudioNoise:
    """
    Class to simplify and encapsulate the code related with audio noise.
    """
    def remove(audio, output_filename: str = None):
        """
        Remove the noise from the provided audio and, if 'output_filename'
        is provided, the audio without noise is written localy with that
        filename.
        """
        # TODO: This fails when .mp3 is used, so we need to transform into wav.
        # TODO: Output file must be also wav
        # TODO: What about audioclip instead of audiofile? Is it possible? (?)
        # Based on this (https://medium.com/@devesh_kumar/how-to-remove-noise-from-audio-in-less-than-10-seconds-8a1b31a5143a)
        # https://github.com/Rikorose/DeepFilterNet
        # TODO: This is failing now saying 'File contains data in an unknon format'...
        # I don't know if maybe some library, sh*t...
        # Load default model
        
        # If it is not an audio filename I need to create it to be able to
        # work with (TODO: Check how to turn into same format as when readed)
        # TODO: Refactor these below to accept any audio, not only filename
        tmp_audio_filename = create_temp_filename('audio_temp.wav')

        audio = AudioParser.to_audiosegment(audio)
        _, tmp_audio_filename = AudioConverter.to_wav(audio, tmp_audio_filename) 

        # TODO: This was done before because the parameter was only
        # a filename and now I'm accepting other audio types
        # if audio_filename.endswith('.mp3'):
        #     # TODO: Maybe it is .wav but not that format...
        #     mp3_to_wav(audio_filename, TMP_WAV_FILENAME)
        #     audio_filename = TMP_WAV_FILENAME

        model, df_state, _ = init_df()
        audio, _ = load_audio(tmp_audio_filename, sr = df_state.sr())
        # Remove the noise
        enhanced = enhance(model, df_state, audio)

        if not output_filename:
            output_filename = create_temp_filename('noise_removed.wav')
        # TODO: Check temp filename extension is valid

        save_audio(output_filename, enhanced, df_state.sr())

        try:
            FileRemover.delete_file(tmp_audio_filename)
        except:
            pass

    # TODO: Create a 'generate' noise method