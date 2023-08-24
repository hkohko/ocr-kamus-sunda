import pytesseract
import cv2 as cv
import re
from os import listdir, mkdir
from os.path import exists
from pathlib import Path
from PIL import Image
from tqdm import tqdm

MAIN_DIR = Path(__file__).parent.parent
IMAGES_DIR = f"{MAIN_DIR}/images"
OUTPUT_TEXT = f"{MAIN_DIR}/text_result"

if not exists(IMAGES_DIR):
    mkdir(IMAGES_DIR)
if not exists(OUTPUT_TEXT):
    mkdir(OUTPUT_TEXT)

tesseract_location = (
    r"C:\Users\rifdi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = tesseract_location


def get_file_number(input_page: int):
    if len(str(input_page)) == 2:
        page = f"0{input_page}"
        return page
    elif len(str(input_page)) == 1:
        page = f"00{input_page}"
        return page
    else:
        return str(input_page)


def processed_img(img: str):
    im = cv.imread(img)
    assert im is not None, "image not found"
    denoised = cv.fastNlMeansDenoising(im, h=5)
    image = Image.fromarray(denoised, "RGB")
    return image


def ocr(im) -> str:
    ocr_result: str = pytesseract.image_to_string(im)
    return ocr_result


def get_sample_image(page: int, subfolder: str):
    str_page = get_file_number(page)
    image_sample = listdir(f"{IMAGES_DIR}/{subfolder}")
    pattern = r"-(\d+)\.\w+"
    for img_text in image_sample:
        match = re.search(pattern, img_text, re.IGNORECASE)
        if match.group(1) == str_page:
            return f"{IMAGES_DIR}/{subfolder}/{img_text}"


def get_pages(subfolder: str, start: int, end: int):
    files = listdir(f"{IMAGES_DIR}/{subfolder}")
    start_page = get_file_number(start)
    end_page = get_file_number(end)
    pattern = r"-(\d+)\.\w+"
    for idx, filename in enumerate(files):
        match = re.search(pattern, filename, re.IGNORECASE)
        if match.group(1) == start_page:
            start_idx = idx
        if match.group(1) == end_page:
            end_idx = idx + 1
    return start_idx, end_idx


def main_all(subfolder: str, start: int, end: int):
    files = listdir(f"{IMAGES_DIR}/{subfolder}")
    start_idx, stop_idx = get_pages(subfolder, start, end)
    with open(f"{OUTPUT_TEXT}/{subfolder}.txt", "a") as save_ocr:
        for idx in tqdm(range(start_idx, stop_idx)):
            filename = files[idx]
            image_path = f"{IMAGES_DIR}/{subfolder}/{filename}"
            prepped_image = processed_img(image_path)
            do_ocr = ocr(prepped_image)
            save_ocr.write(do_ocr)


if __name__ == "__main__":
    # im = processed_img(68, "Kamus_sunda")
    # im.show()
    main_all("Kamus_sunda", 68, 449)
