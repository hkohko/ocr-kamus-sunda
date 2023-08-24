from dataclasses import dataclass
from pathlib import Path
from os import mkdir
from os.path import exists


@dataclass
class Directories:
    MAIN_DIR: str = Path(__file__).parent.parent
    CURRENT_DIR: str = Path(__file__).parent
    IMAGES_DIR: str = f"{MAIN_DIR}/images/"
    PDF_FILES: str = f"{MAIN_DIR}/pdf_files/"
    OUTPUT_TEXT: str = f"{MAIN_DIR}/text_result"


def create_dir():
    if not exists(Directories.IMAGES_DIR):
        mkdir(Directories.IMAGES_DIR)
    if not exists(Directories.PDF_FILES):
        mkdir(Directories.PDF_FILES)
