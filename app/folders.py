from dataclasses import dataclass
from pathlib import PurePath
from os import mkdir
from os.path import exists


@dataclass
class Directories:
    MAIN_DIR: PurePath = PurePath(__file__).parents[1]
    CURRENT_DIR: PurePath = PurePath(__file__).parents[0]
    IMAGES_DIR: str = MAIN_DIR.joinpath("images")
    PDF_FILES: str = MAIN_DIR.joinpath("pdf_files")
    OUTPUT_TEXT: str = MAIN_DIR.joinpath("text_result")


def create_dir():
    if not exists(Directories.IMAGES_DIR):
        mkdir(Directories.IMAGES_DIR)
    if not exists(Directories.PDF_FILES):
        mkdir(Directories.PDF_FILES)
    if not exists(Directories.OUTPUT_TEXT):
        mkdir(Directories.OUTPUT_TEXT)
