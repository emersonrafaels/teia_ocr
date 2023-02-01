from pathlib import Path
from random import choice

from MODEL.image2text import execute_ocr

# SETTING THE DIRECTORY WITH IMAGES TO TEST
dir_images = "TESTS/IMAGES/training_data/images"

# SETTING EXTENSIONS ACCEPTED
types_accepted = (".png", ".jpg")

# GETTING ALL IMAGES
list_all_images = [str(file) for file in Path(dir_images).absolute().iterdir() if file.suffix in types_accepted]

# RANDOM AN IMAGE AMONG ALL
image = choice(list_all_images)

print("SELECTED IMAGE: {}".format(image))

# REQUEST OCR
result_ocr = execute_ocr(image_input=image, view_image=True)

print(result_ocr)
