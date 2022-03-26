from Database.Database import Database
from Database.Word import Word
from Database.DatabaseExceptions import WordNotFoundError
from dataclasses import dataclass
from typing import List
import re

# TODO: Add support for punctuation in translation


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
    mode: bool
    highlight_region: (int, int)


class Translator:
    def __init__(self, text_in: str, db: Database, mode: bool):
        self.split_text = text_in.replace("\n", " ").split(" ")
        self.highlight_regions = []

        i = 0
        for sect in self.split_text:
            self.highlight_regions.append((i, i+len(sect)))
            i += len(sect) + 1

        while True:
            try:
                pos = self.split_text.index("")
                self.split_text.pop(pos)
                self.highlight_regions.pop(pos)
            except ValueError:
                break
        self.db = db

        self.db_all_words = None
        self.translations = None
        self.re_index()

        self.mode = mode
        self.index = 0

    def re_index(self):
        self.db_all_words = self.db.GetAllWords()

        self.translations = {}
        for word in self.db_all_words:
            for s in word.eng_synonyms:
                if s in self.translations.keys():
                    self.translations[s].append(word.name)
                else:
                    self.translations[s] = [word.name]

    def return_builder(self, options: List[str], w: str, highlight_region: (int, int), word_not_found: bool = False) -> TranslationStep:
        return TranslationStep(options, w, word_not_found, self.index, len(self.split_text), self.mode, highlight_region)

    def step(self) -> TranslationStep | None:
        if self.index >= len(self.split_text):
            return None

        w = self.split_text[self.index]
        highlight = self.highlight_regions[self.index]
        if self.mode:
            retrieved_words = {}

            if w in retrieved_words.keys():
                word = retrieved_words[w]
            else:
                try:
                    word = self.db.GetWord(w)
                    retrieved_words[w] = word
                except WordNotFoundError:
                    return self.return_builder([], w, highlight, True)

            return self.return_builder(word.eng_synonyms, w, highlight)
            # if len(word.eng_synonyms) == 0:
            #     return self.return_builder([], w)
            # elif len(word.eng_synonyms) == 1:
            #     return self.return_builder(word.eng_synonyms, w)
            # else:
            #     return self.return_builder(word.eng_synonyms, w)

        else:
            if w not in self.translations.keys():
                return self.return_builder([], w, highlight, True)

            trans = self.translations[w]

            return self.return_builder(trans, w, highlight)
