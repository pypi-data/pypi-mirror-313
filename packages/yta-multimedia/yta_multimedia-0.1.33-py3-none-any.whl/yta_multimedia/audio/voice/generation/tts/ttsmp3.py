from yta_general_utils.downloader import Downloader

import requests


# TODO: Check this because I don't know if this webpage is using the tts (coqui)
# library as the generator engine. If that, I have this engine in 'coqui.py' file
# so I don't need this (that is not stable because is based in http requests)
def narrate_tts3(text: str, output_filename: str):
    """
    This makes a narration based on an external platform. You
    can change some voice configuration in code to make the
    voice different.

    Aparrently not limited. Check, because it has time breaks 
    and that stuff to enhance the narration.
    """
    # From here: https://ttsmp3.com/
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://ttsmp3.com',
        'referer': 'https://ttsmp3.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    VOICES = ['Lupe', 'Penelope', 'Miguel']
    data = {
        'msg': text,
        'lang': 'Lupe',
        'source': 'ttsmp3',
    }

    response = requests.post('https://ttsmp3.com/makemp3_new.php', headers = headers, data = data)
    response = response.json()
    url = response['URL']
    # "https://ttsmp3.com/created_mp3/8b38a5f2d4664e98c9757eb6db93b914.mp3"
    Downloader.download_audio(url, output_filename)