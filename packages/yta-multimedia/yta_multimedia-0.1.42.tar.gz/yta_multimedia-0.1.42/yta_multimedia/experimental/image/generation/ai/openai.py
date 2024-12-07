from yta_general_utils.downloader import Downloader
from yta_general_utils.image.size import resize_without_scaling
from openai import OpenAI


# TODO: Is this actually useful? I think it could be removed...

def generate_image(prompt, output_filename):
    client = OpenAI()

    response = client.images.generate(
        model = "dall-e-3",
        prompt = prompt,
        size = "1792x1024",
        quality = "standard",
        n = 1,
    )

    image_url = response.data[0].url

    Downloader.download_image(image_url, output_filename)
    resize_without_scaling(output_filename)