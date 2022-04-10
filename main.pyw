import setup
# from itertools import chain

from GUI.SetupGui import SetupGui
from logger import *

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    Log("RESFIX", "Resolution fix applied")
except Exception as e:
    Log("RESFIX", f"Resolution fix failed with {type(e).__name__}: {e}", 2)

# NLTK Imports
has_nltk = True
try:
    from nltk.corpus import wordnet
except ImportError:
    has_nltk = False

Log("NLTK", f"Has nltk: {has_nltk}")

setup.setup()

while True:
    SetupGui(has_nltk)
