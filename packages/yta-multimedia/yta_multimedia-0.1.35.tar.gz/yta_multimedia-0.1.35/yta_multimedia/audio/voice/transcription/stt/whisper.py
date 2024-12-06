from faster_whisper import WhisperModel
# TODO: What if 'whisper_timestamped' is better? We should use it
import whisper_timestamped


def get_transcription_text(audio_filename, model = 'base'):
    """
    Receives an 'audio_filename' and gets the transcription of it,
    returning only the text. This is a simple and faster method
    to be used when we simply want the text without timestamps.
    """
    model = WhisperModel(model)

    segments, info = model.transcribe(audio_filename, language = 'es', beam_size = 5)

    text = ""
    for segment in segments:
        text += segment.text + ' '

    text = text.strip()

    return text

# Very interesting (https://github.com/m-bain/whisperX) to get timestamps of each word
# But the one I use is this one (https://github.com/linto-ai/whisper-timestamped)
def get_transcription_with_timestamps(audio_filename, model = 'small', initial_prompt = None):
    """
    Receives an 'audio_filename' and makes a transcription of it, returning a 
    list of 'segments' in the result. You can pass an 'initial_prompt' to help
    the model to recognize some specific words and to have a better performance.

    This method returns a list of the words recognized in the audio with the
    next parameters: 'text' (word string), 'start' (the moment in which that
    word starts being dictated in the audio), 'end' (the moment in which the 
    word stops being dictated in the audio) and 'confidende' (the certainty
    with which the model has recognize that word, from 0 to 1).
    """
    audio = whisper_timestamped.load_audio(audio_filename)
    model = whisper_timestamped.load_model(model, device = "cpu")
    
    # I do this 'initial_prompt' formatting due to some issues when using it 
    # as it was. I read in Cookguide to pass natural sentences like this below
    # and it seems to be working well, so here it is:
    if initial_prompt != None:
        #initial_prompt = '""""' + initial_prompt + '""""'
        #initial_prompt = 'I know exactly what is said in this audio and I will give it to you (between double quotes) to give me the exact transcription. The audio says, exactly """"' + initial_prompt + '""""'
        initial_prompt = 'I will give you exactly what the audio says (the output), so please ensure it fits. The output must be """"' + initial_prompt + '""""'

    # 'vad' = True would remove silent parts to decrease hallucinations
    # 'detect_disfluences' detects corrections, repetitions, etc. so the
    # word prediction should be more accurate. Useful for natural narrations
    result = whisper_timestamped.transcribe(model, audio, language = "es", initial_prompt = initial_prompt)
    
    return result