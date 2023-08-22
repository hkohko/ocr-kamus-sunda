import pytesseract
from os import listdir
from pathlib import Path
from PIL import Image

main_dir = Path(__file__).parent.parent
current_dir = Path(__file__).parent
images_dir = f"{main_dir}/images"
subfolder = "Kamus_sunda"
tesseract_location = (
    r"C:\Users\rifdi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = tesseract_location
page = 173


def get_sample_image():
    image_sample = listdir(f"{images_dir}/Kamus_sunda")
    return image_sample[page + 1]


im = Image.open(f"{images_dir}/{subfolder}/{get_sample_image()}")
print(pytesseract.image_to_string(im))
im.show()
