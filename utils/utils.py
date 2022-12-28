from PIL import Image
from django.conf import settings
from pathlib import Path
import requests


def verify_recaptcha(recaptcha_response):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                             data={
                                 'secret': settings.RECAPTCHA_SECRET_KEY,
                                 'response': recaptcha_response,
                             })

    return response.json()['success']


def resize_image(img_db, new_width=400):
    img_path = settings.MEDIA_ROOT / img_db.name
    with Image.open(img_path) as img:
        width, height = img.size

        if width > new_width:
            new_height = round((height * new_width) / width)

            new_img = img.resize((new_width, new_height), resample=Image.LANCZOS)

            new_img.save(img_path, optimize=True, quality=60)
            new_img.close()
