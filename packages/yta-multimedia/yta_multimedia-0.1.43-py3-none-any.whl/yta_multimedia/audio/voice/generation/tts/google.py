from gtts import gTTS
from enum import Enum

# TODO: Move this to enums.py (?)
class TLD(Enum):
    SPANISH_MEXICO = 'com.mx'
    SPANISH_SPAIN = 'es'
    SPANISH_US = 'us'

class Language(Enum):
    SPANISH = 'es'
    ENGLISH = 'en'

def narrate(text,  language: Language = Language.SPANISH, tld: TLD = TLD.SPANISH_SPAIN, output_filename = None):
    """
    Creates an audio narration of the provided 'text' with the Google voice and stores it
    as 'output_filename'. This will use the provided 'language' language for the narration.
    """
    if not output_filename:
        return None
    # TODO: Check that 'language' and 'tld' are valid
    
    language = language.value
    tld = tld.value
    
    # TODO: Check valid language tag in this table (https://en.wikipedia.org/wiki/IETF_language_tag)
    # TODO: Use this library for languages (https://pypi.org/project/langcodes/)
    # TODO: Here we have the languages and tlds (https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang)
    tts = gTTS(text, lang = language, tld = tld)
    tts.save(output_filename)