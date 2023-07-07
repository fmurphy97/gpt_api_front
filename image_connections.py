import openai
import requests

from PIL import Image
import base64

with open('my apikey.txt', 'r') as file:
    openai.api_key = file.read()


def generate_images(prompt_message, num_images=4, img_size='256x256'):
    """
    Generates images based on an input text
    num_images: number of images we want to generate
    img_size: size of the output images, must be on of ['256x256', '512x512', '1024x1024']
    prompt_message: based on which text we want to generate images
    """
    return openai.Image.create(prompt=prompt_message, n=num_images, size=img_size)


def get_images(response):
    """Based on a response plots images"""
    imgs = []
    for i, resp_i in enumerate(response['data']):
        print(f"This is img #{i}")
        image_url = resp_i['url']
        imgs.append(image_url)

    return imgs


def generate_image_variations(response, resp_id, num_images=4, img_size='256x256'):
    """
    Generates images based on an input image
    num_images: number of images we want to generate
    img_size: size of the output images, must be on of ['256x256', '512x512', '1024x1024']
    prompt_message: based on which text we want to generate images
    """
    return openai.Image.create_variation(
        image=requests.get(response['data'][resp_id]["url"]).content,
        n=num_images,
        size=img_size
    )
