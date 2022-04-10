from nltk.downloader import download as dload
from logger import *


def download():
    Log("NLTK", "Downloading wordnet and omw-1.4")
    dload('wordnet')
    dload('omw-1.4')
