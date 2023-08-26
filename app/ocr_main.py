import pytesseract
import cv2 as cv
import re
from pathlib import Path, PurePath
from app.folders import Directories, create_dir
from os import listdir
from PIL import Image
from tqdm import tqdm

MAIN_DIR = Directories.MAIN_DIR
IMAGES_DIR = Directories.IMAGES_DIR
OUTPUT_TEXT = Directories.OUTPUT_TEXT

create_dir()

tesseract_location = PurePath(Path.home()).joinpath(
    "AppData", "Local", "Programs", "Tesseract-OCR", "tesseract.exe"
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
    print(f"\n\n{img}\n\n")
    im = cv.imread(img)
    assert im is not None, "image not found"
    denoised = cv.fastNlMeansDenoising(im, h=5)
    image = Image.fromarray(denoised, "RGB")
    return image


def ocr(im) -> str:
    ocr_result: str = pytesseract.image_to_string(im)
    return ocr_result


def get_sample_image(page: int, subfolder: str):
    """
    For testing purposes.

    Optimize processed_img() parameter from a sample image.
    """

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


def get_subfolder(folder_name: str):
    subfolders = listdir(IMAGES_DIR)
    for folder in subfolders:
        if folder_name in folder.lower():
            return folder


def main_all(subfolder: str, start: int, end: int, save: bool = True):
    folder_name = get_subfolder(subfolder)
    assert folder_name is not None, "image subfolder doesn't exist"
    image_files = listdir(f"{IMAGES_DIR}/{folder_name}")
    start_idx, stop_idx = get_pages(folder_name, start, end)
    # TODO: write to a database instead
    with open(f"{OUTPUT_TEXT}/{folder_name}.txt", "a") as save_ocr:
        for idx in tqdm(range(start_idx, stop_idx)):
            image_filename = image_files[idx]
            image_path = PurePath(IMAGES_DIR).joinpath(folder_name, image_filename)
            prepped_image = processed_img(str(image_path))
            do_ocr = ocr(prepped_image)
            if save:
                save_ocr.write(do_ocr)


if __name__ == "__main__":
    main_all("kamus", 50, 52)
