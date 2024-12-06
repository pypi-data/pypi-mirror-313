
from yta_general_utils.programming.env import get_current_project_env
from PIL import Image

import requests
import io


class HugginFace:
    """
    Represents the functionality with the HugginFace.co platform that
    has a lot of AI models and API endpoints. Make sure you have the
    'HUGGINFACE_API_KEY' in your .env file, instantiate this class
    with your desired API endpoint, send the payload you need and
    make the magic.

    You go to any existing model in HugginFace platform, then click on
    'Deploy' (on the right side) and 'Inference API' and there you have
    the url and the query structure.
    """
    API_KEY = get_current_project_env("HUGGINFACE_API_KEY")
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}
    
    def __init__(self, api_url):
        self.api_url = api_url

    def __request(self, payload = None, data = None):
        response = requests.post(self.api_url, headers = self.HEADERS, data = data, json = payload)

        return response

    def request_content(self, payload = None, data = None):
        """
        Makes a request with the provided 'payload' and returns
        the '.content' information returned.
        """
        return self.__request(payload = payload, data = data).content

    def request_json(self, payload = None, data = None):
        """
        Makes a request with the provided 'payload' and returns
        the '.json()' information returned.
        """
        return self.__request(payload = payload, data = data).json()
    
    def generate_image(self, payload, output_filename = None):
        """
        Makes a request with the provided payload and stores the 
        image received as response in the local storage as the
        provided 'output_filename'. This method must be used with
        image generation urls.

        This method will store locally the image if 'output_filename'
        provided, and will always return the image read with PIL.

        @param
            **payload**
            The information you need to send in the payload. It 
            depends on the endpoint you are using. It could be 
            just a string or maybe a json (dict). You must check
            it.

        @param
            **output_filename**
            The filename in which you want to store the received
            image if you want to store it. If None provided, it
            wont be stored.
        """
        image_content = self.request_content(payload = payload)

        if output_filename:
            with open(output_filename, 'wb') as outfile:
                outfile.write(image_content)

        return Image.open(io.BytesIO(image_content))













# from PIL import Image

# import requests
# import os
# import io

# API_KEY = os.environ.get("HUGGINFACE_API_KEY")
# HEADERS = {"Authorization": f"Bearer {API_KEY}"}



# def __request(api_url, payload):
#     response = requests.post(api_url, headers = HEADERS, json = payload)
#     print(response)
#     return response

# def __request_image(api_url, payload):
#     return __request(api_url, payload).content

# def __request_json(api_url, payload):
#     return __request(api_url, payload).json()

# def test_image():
#     #API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-cascade'
#     #API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-cascade-prior'
#     #API_URL = 'https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5'
#     #API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1'
#     API_URL = 'https://api-inference.huggingface.co/models/prompthero/openjourney'

#     PAYLOAD = {
#         'inputs': 'Hiperrealistic monk between two cars in the middle of a city'
#     }

#     response = __request_image(API_URL, PAYLOAD)
#     Image.open(io.BytesIO(response)).save('test_tintin.png')

# def test_tintin():
#     API_URL = 'https://api-inference.huggingface.co/models/Pclanglais/TintinIA'

#     PAYLOAD = {
#         'inputs': 'Astronaut riding a horse and holding a coffee'
#     }

#     response = __request_image(API_URL, PAYLOAD)
#     Image.open(io.BytesIO(response)).save('test_tintin.png')

# def test_gemma():
#     API_URL = 'https://api-inference.huggingface.co/models/google/gemma-7b'

#     PAYLOAD = {
#         'inputs': '¿Cuántos habitantes tiene España?'
#     }

#     response = __request_json(API_URL, PAYLOAD)

#     print(response)

# def test():
#     API_URL = 'https://api-inference.huggingface.co/models/deepset/roberta-base-squad2'
    
#     PAYLOAD = {
#         'inputs': {
#             'question': 'What is my name?',
#             'context': 'My name is Clara and I live in Berkeley.',
#         }
#     }

#     response = __request_json(API_URL, PAYLOAD)
#     #response has, in this case, 'answer'
#     print(response)