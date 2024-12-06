import pyttsx3


def narrate(text, output_filename = None):
    """
    Creates an audio narration of the provided 'text' and stores it as 'output_filename'.
    """
    if not output_filename:
        return None
    
    # TODO: This is hardcoded, be careful!
    SPANISH_SPAIN_VOICE_ID = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
    SPANISH_MEXICO_VOICE_ID = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
    engine = pyttsx3.init()
    engine = pyttsx3.init()
    engine.setProperty('voice', SPANISH_SPAIN_VOICE_ID)
    # Default speed is 200 (wpm)
    engine.setProperty('rate', 130)
    engine.save_to_file(text, output_filename)
    engine.runAndWait()