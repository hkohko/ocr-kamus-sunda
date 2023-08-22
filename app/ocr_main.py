import pytesseract
import cv2 as cv
from io import BytesIO
from os import listdir
from pathlib import Path
from PIL import Image, ImageEnhance

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
    return f"{images_dir}/{subfolder}/{image_sample[page + 1]}"


def adapt_thresh():
    img = cv.imread(get_sample_image())
    # img = cv.medianBlur(img, 5)
    # _,thresh1 = cv.threshold(img,thresh=245, maxval=255, type=cv.THRESH_BINARY)
    # th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    img = cv.fastNlMeansDenoising(img, h=5)
    image = Image.fromarray(img, "RGB")
    return image


if __name__ == "__main__":
    im = adapt_thresh()
    print(pytesseract.image_to_string(im))
    im.show()
