import os
import pathlib


def readfile(path):
    with open(path, 'r') as fh:
        contents = fh.read()
    return contents.strip()


PKG_DIR = str(pathlib.Path(__file__).parent.resolve())
VERSION = readfile(os.path.sep.join([PKG_DIR, 'VERSION']))
