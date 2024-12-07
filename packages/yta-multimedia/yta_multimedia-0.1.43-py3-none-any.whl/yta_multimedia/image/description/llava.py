"""
1. You need to install Ollama to handle llama models. Just download
and install from this website: https://ollama.com

# This one (https://www.youtube.com/watch?v=EBUMxu2hl34) says that
you can use openai.chat to communicate to the ollama model

2. You must install 'ollama' python package to communicate with the
models you download and use

# Based on this (https://www.youtube.com/watch?v=4Jpltb9crPM) I am
not able to execute it because it never ends loading llava I think

https://llava-vl.github.io/
"""
import ollama


def describe_image_NOT_WORKING(image_filename: str):
    """
    This method will return a description of the provided 
    'image_filename' based on the ollama 'llava' model.

    TODO: This is not working because of my pc limitations.
    It cannot load the resources due to memory capacity.
    """
    res = ollama.chat(
        model = 'llava',
        messages = [
            {
                'role': 'user',
                'content': 'Describe this image',
                'images': [
                    image_filename
                ]
            }
        ]
    )

    response_content = res['message']['content']

    return response_content

# print('here trying to')
# path = 'C:/Users/dania/Desktop/suscribirte_imagen_guapa.png'
# print(describe_image(path))
# print('ended?')