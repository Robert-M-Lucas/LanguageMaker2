from Database.Database import Database
from Database.DatabaseExceptions import WordNotFoundError
import re


def Translate(text_in: str, db: Database) -> str:
    split_text = text_in.replace("\n", " ").split(" ")
    while True:
        try:
            split_text.remove("")
        except ValueError:
            break
    out_str = ""

    retrieved_words = {}

    for w in split_text:
        if w in retrieved_words.keys():
            word = retrieved_words[w]
        else:
            try:
                word = db.GetWord(w)
                retrieved_words[w] = word
            except WordNotFoundError:
                out_str += f"[{w} doesn't exist] "
                continue

        if len(word.eng_synonyms) == 0:
            out_str += f"[NT for {w}]"
        elif len(word.eng_synonyms) == 1:
            out_str += word.eng_synonyms[0]
        else:
            out_str += "[" + "/".join([x for x in word.eng_synonyms]) + "]"
        out_str += " "

    return out_str

