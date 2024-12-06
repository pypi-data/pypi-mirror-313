
from yta_general_utils.programming.env import get_current_project_env
from elevenlabs import generate, save, set_api_key


API_KEY = get_current_project_env('ELEVENLABS_API_KEY')

# TODO: Implement a method to get an existing voice attending to a 'type' (terror, inspirational, etc.)

def generate_elevenlabs_narration(text, voice, output_filename):
    """
    Receives a 'text' and generates a single audio file with that 'text' narrated with
    the provided 'voice', stored locally as 'output_filename'.

    This method will split 'text' if too much longer to be able to narrate without issues
    due to external platform working process. But will lastly generate a single audio file.
    """
    texts = [text]
    # TODO: Set this limit according to voice type
    if len(text) > 999999:
        texts = []
        # TODO: Handle splitting text into subgroups to narrate and then join
        print('No subgrouping text yet')
        texts = [text]

    if len(texts) == 1:
        # Only one single file needed
        download_elevenlabs_audio(texts[0], voice, output_filename)
    else:
        for text in texts:
            # TODO: Generate single file
            print('Not implemented yet')

        # TODO: Join all generated files in only one (maybe we need some silence in between?)
            
    return output_filename

def download_elevenlabs_audio(text = 'Esto es API', voice = 'Freya', output_file = 'generated_elevenlabs.wav'):
    """
    Generates a narration in elevenlabs and downloads it as output_file audio file.
    """
    set_api_key(API_KEY)
    # TODO: Check if voice is valid
    # TODO: Check which model fits that voice.
    model = 'eleven_multilingual_v2'

    if not output_file.endswith('.wav'):
        output_file = output_file + '.wav'

    # TODO: Try to be able to call it with stability parameter
    audio = generate(
        text = text,
        voice = voice,
        model = model
    )

    save(audio, output_file)