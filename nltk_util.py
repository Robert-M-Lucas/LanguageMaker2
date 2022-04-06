from nltk.downloader import download as dload

from logger import *

def download():
    Log("NLTK", "Downloading nltk")
    dload('wordnet')
