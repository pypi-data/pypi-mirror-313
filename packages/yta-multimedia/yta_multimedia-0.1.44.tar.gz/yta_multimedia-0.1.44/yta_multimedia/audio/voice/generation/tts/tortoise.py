from TTS.api import TTS


def narrate(text, output_filename):
    """
    @deprecated

    TODO: Remove this file and method if useless. Please, read below to check.
    This method should be removed and also the file as it is only one specific
    model in TTS narration library. It is not a different system. So please,
    remove it if it won't be used.
    """
    # TODO: Delete tortoise lib?
    # TODO: Delete en/multi-datase/tortoise-v2 model
    tts = TTS("tts_models/es/multi-dataset/tortoise-v2")
    # Check code here: https://docs.coqui.ai/en/latest/models/tortoise.html
    tts.tts_to_file(text = text, language = 'es', file_path = output_filename)

    #reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    
    #pcm_audio = tts.tts(text)
    #pcm_audio = tts.tts_with_preset("your text here", voice_samples=reference_clips, preset='fast')
    
    #from tortoise.utils.audio import load_audio, load_voice