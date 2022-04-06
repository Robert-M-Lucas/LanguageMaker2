import setup
# from itertools import chain

from GUI.SetupGui import SetupGui
from logger import *

# NLTK Imports
has_nltk = True
try:
    from nltk.corpus import wordnet
except ImportError:
    has_nltk = False

Log("NLTK", f"Has nltk: {has_nltk}")

setup.setup()

# synonyms = wordnet.synsets("good")
# lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
# print(lemmas)

while True:
    SetupGui(has_nltk)
