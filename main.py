from pathlib import Path
from random import choice

from MODEL.image2text import execute_ocr

# DEFININDO O DIRETÓRIO CONTENDO IMAGES PARA TESTE
dir_images = "TESTS/IMAGES/training_data/images"

# DEFININDO OS TIPOS DE ARQUIVOS DESEJADOS
types_accepted = (".png", ".jpg")

# OBTENDO TODAS AS IMAGENS
list_all_images = [str(file) for file in Path(dir_images).absolute().iterdir() if file.suffix in types_accepted]

# OBTENDO UMA IMAGEM DE FORMA ALEATÓRIA
image = choice(list_all_images)

print("SELECTED IMAGE: {}".format(image))

# SOLICITANDO O OCR
result_ocr = execute_ocr(image_input=image, view_image=True)

print(result_ocr)
