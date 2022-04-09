import os
import sys

from logger import *

ALLOWED_LANG_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def exit(code=0):
    Log("General", "Exiting", 1)
    sys.exit(code)
