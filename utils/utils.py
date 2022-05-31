from PIL import Image
from django.conf import settings
from pathlib import Path


def resize_image(img_db, new_width: 400):
    img_path = settings.MEDIA_ROOT / img_db.name
    with Image.open(img_path) as img:
        width, height = img.size()

        if width > new_width:
            new_height = round((height * new_width) / width)

            new_img = img.resize((new_width, new_height), resample=Image.LANCZOS)

            new_img.save(img_path, optimize=True, quality=60)
            new_img.close()
