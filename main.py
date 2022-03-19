from itertools import chain
from GUI.SetupGui import SetupGui

# NLTK Imports
has_nltk = True
try:
    from nltk.corpus import wordnet
except ImportError:
    has_nltk = False

# synonyms = wordnet.synsets("good")
# lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
# print(lemmas)

SetupGui(has_nltk)
