from yta_general_utils.downloader import Downloader
from yta_general_utils.image.size import resize_without_scaling
from yta_general_utils.programming.env import get_current_project_env

import requests
import time


MODEL_LEONARDO_DIFFUSION_XL = '1e60896f-3c26-4296-8ecc-53e2afecc132'

def __generate_image(prompt):
    """
    Makes a request to generate an image. It returns the generation id.

    This method needs the non-free API working.
    """
    #return '69503ef1-85c8-41cc-b292-f672946920d7'
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        'modelId': MODEL_LEONARDO_DIFFUSION_XL,
        'width': 1024,   # test 1536
        'height': 576,   # test 864
        'num_images': 1,
        'prompt': prompt
    }

    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + str(get_current_project_env('LEONARDOAI_API_KEY')),
        "content-type": "application/json",
    }

    response = requests.post(url, json = payload, headers = headers)
    response = response.json()

    print(response)

    return response['sdGenerationJob']['generationId']

def __download_generated_image(generation_id, output_filename):
    """
    Downloads the AI-generated image by using the provided 'generation_id'.

    It downloads the image and resizes it to 1920x1080.
    """
    url = 'https://cloud.leonardo.ai/api/rest/v1/generations/' + str(generation_id)

    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + str(get_current_project_env('LEONARDOAI_API_KEY')),
    }

    response = requests.get(url, headers = headers)
    response = response.json()

    # TODO: Do a passive waiting
    is_downloadable = True

    if len(response['generations_by_pk']['generated_images']) == 0:
        is_downloadable = False

    while not is_downloadable:
        time.sleep(10)
        print('Doing a request in loop')

        # We do the call again
        response = requests.get(url, headers = headers)
        response = response.json()
        
        if len(response['generations_by_pk']['generated_images']) > 0:
            is_downloadable = True

    downloadable_url = response['generations_by_pk']['generated_images'][0]['url']

    Downloader.download_image(downloadable_url, output_filename)
    resize_without_scaling(output_filename)

def generate_image(prompt, output_filename):
    """
    Generates an AI image with the provided 'prompt' and stores it locally
    as the 'output_filename'.
    """
    generation_id = __generate_image(prompt)
    __download_generated_image(generation_id, output_filename)

