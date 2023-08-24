from pdf2image import convert_from_path
from pathlib import Path
from os import listdir, mkdir
import logging

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

MAIN_DIR = Path(__file__).parent.parent
CURRENT_DIR = Path(__file__).parent
IMAGES_DIR = f"{MAIN_DIR}/images/"


def create_images_dir():
    if "images" not in listdir(MAIN_DIR):
        mkdir(IMAGES_DIR)


def get_pdf_file(filename: str):
    pdf_dir = [
        file for file in listdir(f"{MAIN_DIR}/pdf_files/") if file[-4:] == ".pdf"
    ]
    for pdf in pdf_dir:
        if filename in pdf.lower():
            return pdf


def create_images_subfolder(filename: str):
    if filename not in listdir(IMAGES_DIR):
        mkdir(f"{IMAGES_DIR}/{filename}")
        logger.info(f"created subfolder: {filename}")


def get_poppler_path():
    poppler_folder = next(folder for folder in listdir(MAIN_DIR) if "poppler" in folder)
    if poppler_folder is None:
        logger.warning("get_poppler_path: poppler path not found")
        raise ValueError
    logger.info("getting poppler path")
    return poppler_folder


def convert_to_image(filename: str):
    create_images_dir()
    pdf_file = get_pdf_file(filename)
    folder_name = pdf_file[:-4]
    create_images_subfolder(folder_name)
    pdf_path = f"{MAIN_DIR}/pdf_files/{pdf_file}"
    poppler_path = rf"{MAIN_DIR}/{get_poppler_path()}/Library/bin/"
    output_folder = f"{MAIN_DIR}/images/{folder_name.lower()}/"
    if pdf_file in listdir(IMAGES_DIR):
        logger.info("subfolder already created")
    logger.info("converting to images...")
    convert_from_path(
        pdf_path=pdf_path,
        poppler_path=poppler_path,
        output_folder=output_folder,
        fmt="jpeg",
        use_cropbox=True,
    )
    return


if __name__ == "__main__":
    convert_to_image("kamus_sunda")
