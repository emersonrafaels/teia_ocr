<h1 align="center">
    <img alt="TEIA OCR" title="#TEIAOCR" src="./ASSETS/banner.png" />
</h1>

<h4 align="center"> 
	🚧 TEIA OCR 1.0 🚀 em desenvolvimento... 🚧
</h4>

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/emersonrafaels/teia_ocr?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/emersonrafaels/teia_ocr">

  	
  <a href="https://www.linkedin.com/in/emerson-rafael/">
    <img alt="Siga no Linkedin" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
  </a>
	
  
  <a href="https://github.com/emersonrafaels/teia_ocr/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/emersonrafaels/teia_ocr">
  </a>

  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
   <a href="https://github.com/emersonrafaels/teia_ocr/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/emersonrafaels/teia_ocr?style=social">
  </a>
</p>


## 💻 About the project

📦 

## 🛠  Technologies


- [Python]

## 🚀 How to execute the project

1. **Install**: pip install -r requirements.txt

Ex: Execution Example:

```python
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

```

## ➊ Requirements


## [≝] Tests


## 📝 License

This project is under MIT License.

Developed ❤️ by **Emerson Rafael** 👋🏽 [Contact me!](https://www.linkedin.com/in/emerson-rafael/)

[Python]: https://www.python.org/downloads/