from TTS.api import TTS


# TODO: From here (https://github.com/coqui-ai/TTS)
def narrate(text, output_filename = None):
    """
    Generates a narration audio file with the provided 'text' that
    will be stored as 'output_filename' file.

    This method uses a Spanish model so 'text' must be in Spanish.

    This method will take some time to generate the narration.
    """
    if not output_filename:
        return None
    
    # tts_es_fastpitch_multispeaker.nemo
    # These below are the 2 Spanish models that exist
    SPANISH_MODEL_A = 'tts_models/es/mai/tacotron2-DDC'
    SPANISH_MODEL_B = 'tts_models/es/css10/vits'
    tts = TTS(model_name = SPANISH_MODEL_B)
    tts.tts_to_file(text = text, file_path = output_filename)

def narrrate_imitating_voice(text, input_filename = None, output_filename = None):
    """
    Narrates the provided 'text' by imitating the provided 'input_filename'
    audio file (that must be a voice narrating something) and saves the 
    narration as 'output_filename'.

    The 'input_filename' could be an array of audio filenames.

    Language is set 'es' in code by default.

    This method will take time as it will recreate the voice parameters with
    which the narration will be created after that.

    ANNOTATIONS: This method is only copying the way the narration voice 
    talks, but not the own voice. This is not working as expected, as we are
    not cloning voices, we are just imitating the tone. We need another way
    to actually clone the voice as Elevenlabs do.
    """
    if not input_filename:
        return None
    if not output_filename:
        return None

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    # This below will use the latest XTTS_v2 (needs to download the model)
    #tts = TTS('xtts')

    # TODO: Implement a way of identifying and storing the voices we create to
    # be able to use again them without recreating them twice.

    # input_filename can be an array of wav files
    # generate speech by cloning a voice using default settings
    tts.tts_to_file(text = text, file_path = output_filename, speaker_wav = input_filename, language = 'es')