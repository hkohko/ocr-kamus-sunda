import pytesseract
import cv2 as cv
import re
from os import listdir
from pathlib import Path
from PIL import Image

main_dir = Path(__file__).parent.parent
current_dir = Path(__file__).parent
images_dir = f"{main_dir}/images"

tesseract_location = (
    r"C:\Users\rifdi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = tesseract_location


def get_sample_image():
    subfolder = "Kamus_sunda"
    page = 68

    if len(str(page)) == 2:
        page = f"0{page}"
    elif len(str(page)) == 1:
        page = f"00{page}"

    image_sample = listdir(f"{images_dir}/{subfolder}")
    pattern = r"-(\d+)\.\w+"
    for img_text in image_sample:
        match = re.search(pattern, img_text, re.IGNORECASE)
        if match.group(1) == page:
            return f"{images_dir}/{subfolder}/{img_text}"


def processed_img():
    img = cv.imread(get_sample_image())
    img = cv.fastNlMeansDenoising(img, h=5)
    image = Image.fromarray(img, "RGB")
    return image


if __name__ == "__main__":
    im = processed_img()
    print(pytesseract.image_to_string(im))
    im.show()
