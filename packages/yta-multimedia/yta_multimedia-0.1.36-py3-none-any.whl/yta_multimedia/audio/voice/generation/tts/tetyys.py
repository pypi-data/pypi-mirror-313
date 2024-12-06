from yta_general_utils.file.writer import FileWriter

import requests


def narrate_tetyys(text: str, output_filename: str):
    """
    This method creates an audio voice narration of the provided
    'text' read with tthe tetyys system voice (Microsoft Speech
    API 4.0 from 1998) and stores it as 'output_filename'. It is 
    only available for ENGLISH speaking.

    You can change some voice parameters in code to make it a
    different voice.

    This method is requesting an external (but apparently stable
    website).
    """
    # This was taken from here (https://www.tetyys.com/SAPI4/)
    if not text:
        return None
    
    if not output_filename:
        return None
    
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.tetyys.com/SAPI4/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    params = {
        'text': text,
        # Inspect options 'value' from https://www.tetyys.com/SAPI4/ but
        # each voice has a pre-set 'pitch' and 'speed' 
        'voice': 'Sam', 
        'pitch': '100',
        'speed': '150',
    }

    """
    Some VOICE options:
        'Male Whisper' 113, 140
        'Female Whisper' 169, 140
        'Mary' 169, 140
        'Mary in Space'|'Mary in Hall'|'Mary in Stadium'|Mary (for Telephone) 169, 140
        'Mike in Space'|... 113, 140
        'RobosoftOne'|'RobosoftTwo'
        'Sam' 100, 140
    """

    response = requests.get('https://www.tetyys.com/SAPI4/SAPI4', params = params, headers = headers)

    FileWriter.write_binary_file(response.content, output_filename)

    return output_filename