from os import chdir
from pathlib import PurePath
from app.folders import create_dir
chdir(PurePath(__file__).parent)
create_dir()
