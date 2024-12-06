from yta_general_utils.image.parser import ImageParser
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Union


def describe_image(image: Union[str, Image.Image]):
    """
    Describes the provided 'image' by using the Salesforce blip 
    image captioning system. This method will use some
    pretrained models that are stored in 
    'C:/Users/USER/.cache/huggingface/hub', load in memory and used
    to describe the image. This process could take a couple of 
    minutes.
    """
    image = ImageParser.to_pillow(image)

    # models are stored in C:\Users\USERNAME\.cache\huggingface\hub
    processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
    model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')
    inputs = processor(image, return_tensors = 'pt')
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokes = True)

    # TODO: Fix strange characters. I received 'a red arrow pointing up
    # to the right [SEP]' response from describing an image. What is the
    # '[SEP]' part? What does it mean? I don't want that in response.
    return description