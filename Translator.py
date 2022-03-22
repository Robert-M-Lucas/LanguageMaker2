from Database.Database import Database
from Database.DatabaseExceptions import WordNotFoundError
from dataclasses import dataclass
from typing import List
import re


def TranslateAll(text_in: str, db: Database, mode: bool) -> str:
    split_text = text_in.replace("\n", " ").split(" ")
    while True:
        try:
            split_text.remove("")
        except ValueError:
            break
    out_str = ""

    if mode:
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

    else:
        translations = {}
        for w in db.GetAllWords():
            for s in w.eng_synonyms:
                if s in translations.keys():
                    translations[s].append(w.name)
                else:
                    translations[s] = [w.name]

        for w in split_text:
            if w not in translations.keys():
                out_str += f"[NT for {w}] "
                continue
            trans = translations[w]
            if len(trans) == 1:
                out_str += trans[0]
            else:
                out_str += "[" + "/".join([x for x in trans]) + "]"
            out_str += " "

    return out_str


@dataclass
class TranslationStep:
    translation_options: List[str]
    source_word: str
    word_not_found: bool
    current_word: int
    total_words: int


class Translator:
    def __init__(self, text_in: str, db: Database, mode: bool):
        self.split_text = text_in.replace("\n", " ").split(" ")
        while True:
            try:
                self.split_text.remove("")
            except ValueError:
                break
        self.db = db
        self.db_all_words = self.db.GetAllWords()
        self.mode = mode
        self.index = 0

    def return_builder(self, options: List[str], w: str, word_not_found: bool = False) -> TranslationStep:
        self.index += 1
        return TranslationStep(options, w, word_not_found, self.index, len(self.split_text))

    def step(self) -> TranslationStep | None:
        if self.index >= len(self.split_text):
            return None

        w = self.split_text[self.index]
        if self.mode:
            retrieved_words = {}

            if w in retrieved_words.keys():
                word = retrieved_words[w]
            else:
                try:
                    word = self.db.GetWord(w)
                    retrieved_words[w] = word
                except WordNotFoundError:
                    return self.return_builder([], w, True)

            return self.return_builder(word.eng_synonyms, w)
            # if len(word.eng_synonyms) == 0:
            #     return self.return_builder([], w)
            # elif len(word.eng_synonyms) == 1:
            #     return self.return_builder(word.eng_synonyms, w)
            # else:
            #     return self.return_builder(word.eng_synonyms, w)

        else:
            translations = {}
            for w in self.db_all_words:
                for s in w.eng_synonyms:
                    if s in translations.keys():
                        translations[s].append(w.name)
                    else:
                        translations[s] = [w.name]

            if w not in translations.keys():
                return self.return_builder([], w, True)
            trans = translations[w]

            return self.return_builder(trans, w)
