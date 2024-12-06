from yta_general_utils.programming.path import get_project_abspath
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS
from pathlib import Path

import os
import torch


PROJECT_ABSOLUTE_PATH = get_project_abspath()

def narrate(text, speed = 1.0, output_filename = None):
    """
    Narrates the provided 'text' at the provided 'speed' with the MeloTTS
    library. The file will be saved as 'output_filename'.

    # TODO: @definitive_cantidate
    """
    if not output_filename:
        return None
    
    # TODO: Check if speed is valid
    
    # This below will automatically choose GPU if available
    device = 'auto' 
    model = TTS(language = 'ES', device = device)
    speaker_ids = model.hps.data.spk2id
    model.tts_to_file(text, speaker_ids['ES'], output_filename, speed = speed)

def clone_voice(input_filename):
    CHECKPOINTS_PATH = (Path(__file__).parent.parent.__str__() + '/resources/openvoice/checkpoints_v2/').replace('\\', '/')
    
    ckpt_converter = CHECKPOINTS_PATH + 'converter'
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device = device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
    source_se = torch.load(f'{CHECKPOINTS_PATH}/base_speakers/ses/es.pth', map_location = device)
    # This will generate a 'se.pth' file and some wavs that are the cloned voice
    target_se, audio_name = se_extractor.get_se(input_filename, tone_color_converter, vad = False)


def imitate_voice(text, input_filename = None, output_filename = None):
    """
    This method imitates the 'input_filename' provided voice and
    generates a new narration of the provided 'text' and stores it
    as 'output_filename'.

    The provided 'input_filename' must be a valid audio file that
    contains a clear narration to be imitated.

    # TODO: @definitive_cantidate
    """
    if not input_filename:
        return None
    
    if not output_filename:
        return None
    
    CHECKPOINTS_PATH = (Path(__file__).parent.parent.__str__() + '/resources/openvoice/checkpoints_v2/').replace('\\', '/')
    
    ckpt_converter = CHECKPOINTS_PATH + 'converter'
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device = device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    source_se = torch.load(f'{CHECKPOINTS_PATH}/base_speakers/ses/es.pth', map_location = device)
    target_se, audio_name = se_extractor.get_se(input_filename, tone_color_converter, vad = False)

    # This below is for testing
    # audio_segs is the number of audio segments created
    # se_save_path is the path in which se.pth file has been saved
    # TODO: Need to know the path in which everything is saved to detect audio
    # segments number and also to be able to load the 'se.pth' file
    path = PROJECT_ABSOLUTE_PATH + 'processed/narracion_irene_albacete_recortado_v2_OMR2KXcN3jYVFUsb'
    tone_color_converter.extract_se(30, se_save_path = path), 'narracion_irene_albacete_recortado_v2_OMR2KXcN3jYVFUsb'
    # TODO: Check what is 'target_se' to check if it is a string and we can
    # point the 'se.pth' file, because I don't already understand how it works
    # This above is for testing

    # We generate a narration to obtain it but with the 'input_filename' voice
    source_filename = 'tmp.wav'
    narrate(text, output_filename = source_filename)

    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path = source_filename, 
        src_se = source_se, 
        tgt_se = target_se, 
        output_path = output_filename,
        message = encode_message)
    
    # TODO: Remove tmp file 'source_filename'
    try:
        os.remove('tmp.wav')
    except:
        pass



def __test():
    # TODO: This must be deleted, I keep it to ensure nothing will fail in the future
    # TODO: Took from here (https://github.com/myshell-ai/OpenVoice/blob/main/demo_part3.ipynb)
    PATH = 'C:/Users/dania/Desktop/PROYECTOS/yta-ai-utils/yta_ai_utils/'

    ckpt_converter = PATH + 'resources/openvoice/checkpoints_v2/converter'
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    output_dir = 'output/openvoice'

    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device = device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    os.makedirs(output_dir, exist_ok = True)

    reference_speaker = PATH + 'resources/test.m4a' # This is the voice you want to clone
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad = False)

    texts = {
        'EN_NEWEST': "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
        'EN': "Did you ever hear a folk tale about a giant turtle?",
        'ES': "El resplandor del sol acaricia las olas, pintando el cielo con una paleta deslumbrante.",
        'FR': "La lueur dorée du soleil caresse les vagues, peignant le ciel d'une palette éblouissante.",
        'ZH': "在这次vacation中，我们计划去Paris欣赏埃菲尔铁塔和卢浮宫的美景。",
        'JP': "彼は毎朝ジョギングをして体を健康に保っています。",
        'KR': "안녕하세요! 오늘은 날씨가 정말 좋네요.",
    }

    src_path = f'{output_dir}/tmp.wav'

    # Basic (no cloning) below
    speed = 1.0

    for language, text in texts.items():
        model = TTS(language=language, device=device)
        speaker_ids = model.hps.data.spk2id
        
        for speaker_key in speaker_ids.keys():
            speaker_id = speaker_ids[speaker_key]
            speaker_key = speaker_key.lower().replace('_', '-')
            
            source_se = torch.load(f'{PATH}checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
            model.tts_to_file(text, speaker_id, src_path, speed = speed)
            save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

            # Run the tone color converter
            encode_message = "@MyShell"
            tone_color_converter.convert(
                audio_src_path=src_path, 
                src_se=source_se, 
                tgt_se=target_se, 
                output_path=save_path,
                message=encode_message)