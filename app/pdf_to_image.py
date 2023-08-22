from pdf2image import convert_from_path
from pathlib import Path
from os import listdir, mkdir
from pypdf import PdfReader
import logging

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
main_dir = Path(__file__).parent.parent
current_dir = Path(__file__).parent
images_dir = f"{main_dir}/images/"


def create_images_dir():
    if "images" not in listdir(main_dir):
        mkdir(images_dir)


def get_pdf_file(filename: str):
    pdf_dir = [
        file for file in listdir(f"{main_dir}/pdf_files/") if file[-4:] == ".pdf"
    ]
    for pdf in pdf_dir:
        if filename in pdf.lower():
            return pdf


def page_size(filename: str):
    pdf_name = get_pdf_file(filename)
    if pdf_name is None:
        logger.warning("page_size: no pdf found with that name")
        raise ValueError
    file = f"{main_dir}/pdf_files/{pdf_name}"
    reader = PdfReader(file)
    box = reader.pages[0].mediabox
    width = box.width
    height = box.height
    logger.info("getting page size")
    return (width, height)


def create_images_subfolder(filename: str):
    if filename not in listdir(images_dir):
        mkdir(f"{images_dir}/{filename}")
        logger.info(f"created subfolder: {filename}")


def get_poppler_path():
    poppler_folder = next(folder for folder in listdir(main_dir) if "poppler" in folder)
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
    pdf_path = f"{main_dir}/pdf_files/{pdf_file}"
    poppler_path = rf"{main_dir}/{get_poppler_path()}/Library/bin/"
    output_folder = f"{main_dir}/images/{folder_name.lower()}/"
    if pdf_file in listdir(images_dir):
        logger.info("subfolder already created")
    logger.info("converting to images...")
    convert_from_path(
        pdf_path=pdf_path,
        poppler_path=poppler_path,
        output_folder=output_folder,
        fmt="jpeg",
        use_cropbox=True
    )
    return


if __name__ == "__main__":
    convert_to_image("kamus_sunda")
