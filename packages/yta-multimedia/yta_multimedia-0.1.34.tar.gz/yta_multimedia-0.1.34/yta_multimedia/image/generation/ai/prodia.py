from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.downloader import Downloader

import time
import requests


PRODIA_API_KEY =  get_current_project_env('PRODIA_API_KEY')

def generate_image_with_prodia(prompt: str, output_filename: str):
    """
    Generates a new prodia image with the provided 'prompt' and stores it
    locally with the provided 'output_filename'.
    """
    # url = 'https://api.prodia.com/v1/sdxl/generate'

    # Landscape ar = 1344x768 | Vertical ar = 768x1344

    # This below returns a response containing the job working on navigator 
    # and allows me using other models as generators
    # I can inspect here (https://app.prodia.com/) and see model strings
    # https://api.prodia.com/generate?new=true&prompt=a+woman&model=absolutereality_v181.safetensors+%5B3d9d4d2b%5D&negative_prompt=&steps=20&cfg=7&seed=2328045384&sampler=DPM%2B%2B+2M+Karras&aspect_ratio=square
    # {"job":"acffa9a4-6d59-44c0-9f37-bdf1fc5da1c6","status":"queued","params":{"type":"TextToImage","options":{"sd_model_checkpoint":"absolutereality_v181.safetensors [3d9d4d2b]"},"request":{"prompt":"a woman","cfg_scale":7,"steps":20,"negative_prompt":"","seed":2328045384,"sampler_name":"DPM++ 2M Karras","width":512,"height":512}}}

    # payload = {
    #     'new': True,
    #     'prompt': prompt,
    #     #'model': 'absolutereality_v181.safetensors [3d9d4d2b]',   # this model works on above request, not here
    #     'model': 'sd_xl_base_1.0.safetensors [be9edd61]',
    #     #'negative_prompt': '',
    #     'steps': 20,
    #     'cfg_scale': 7,
    #     'seed': 2328045384,
    #     'sampler': 'DPM++ 2M Karras',
    #     'width': 1344,
    #     'height': 768
    # }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json",
    #     "X-Prodia-Key": PRODIA_API_KEY
    # }
    if not prompt:
        return None
    
    if not output_filename:
        return None

    # If you comment this and uncomment the one below it works
    # seed = randint(1000000000, 9999999999)
    # response = requests.get('https://api.prodia.com/generate?new=true&prompt=' + prompt + '&model=absolutereality_v181.safetensors+%5B3d9d4d2b%5D&steps=20&cfg=7&seed=' + str(seed) + '&sampler=DPM%2B%2B+2M+Karras&aspect_ratio=square')
    payload = {
        'new': True,
        'prompt': prompt,
        #'model': 'absolutereality_v181.safetensors [3d9d4d2b]',   # this model works on above request, not here
        'model': 'sd_xl_base_1.0.safetensors [be9edd61]',
        #'negative_prompt': '',
        'steps': 20,
        'cfg_scale': 7,
        'seed': 2328045384,
        'sampler': 'DPM++ 2M Karras',
        'width': 1344,
        'height': 768
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": PRODIA_API_KEY
    }
    url = 'https://api.prodia.com/v1/sdxl/generate'
    response = requests.post(url, json = payload, headers = headers)
    response = response.json()

    # When requested it is queued, so we ask for it until it is done
    if "status" in response and response['status'] == 'queued':
        job_id = response['job']
        __retrieve_job(job_id, output_filename)
    else:
        print(response)

def __retrieve_job(job_id, output_filename):
    """
    Makes a request for the image that is being generated with the
    provided 'job_id'.

    It has a loop to wait until it is done. This code is critic.
    """
    url = "https://api.prodia.com/v1/job/" + str(job_id)

    headers = {
        "accept": "application/json",
        "X-Prodia-Key": PRODIA_API_KEY
    }

    response = requests.get(url, headers = headers)
    response = response.json()
    #print(response)

    # TODO: Do a passive waiting
    is_downloadable = True

    if response['status'] != 'succeeded':
        is_downloadable = False

    # TODO: Implement a tries number
    while not is_downloadable:
        time.sleep(5)
        print('Doing a request in loop')

        # We do the call again
        response = requests.get(url, headers = headers)
        response = response.json()
        print(response)
        if 'imageUrl' in response:
            is_downloadable = True

    image_url = response['imageUrl']

    return Downloader.download_image(image_url, output_filename)