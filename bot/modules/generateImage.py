import base64
import os
from aiogram.types import FSInputFile

async def generateImage(generated_images, user_name):
    if not generated_images:
        return None

    directory = 'models/generateImage/images'
    os.makedirs(directory, exist_ok=True)

    photos = []

    for idx, img_base64 in enumerate(generated_images):
        file_number = idx + 1
        file_path = os.path.join(directory, f"image_from_{user_name}_#{file_number}.jpg")


        while os.path.exists(file_path):
            file_number += 1
            file_path = os.path.join(directory, f"image_from_{user_name}_#{file_number}.jpg")


        with open(file_path, "wb") as file:
            file.write(base64.b64decode(img_base64))


        photo = FSInputFile(file_path)
        photos.append(photo)

    return photos