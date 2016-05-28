import requests

from PIL import Image
from io import BytesIO


def get_image_width(url):
    try:
        data = requests.get(url).content
        im = Image.open(BytesIO(data))
        return im.size[0]
    except requests.exceptions.RequestException as e:
        return 0


def get_biggest_images(images):
    biggest_photo_url = None
    biggest_photo_width = 0
    for image in images:
        if 'src' in image:
            width = get_image_width(image['src'])
            if width > biggest_photo_width:
                biggest_photo_width = width
                biggest_photo_url = image['src']
    return biggest_photo_url

