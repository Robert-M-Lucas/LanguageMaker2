from Database.Database import Database
from Database.Word import Word
from Database.DatabaseExceptions import WordNotFoundError
from logger import *

from dataclasses import dataclass
from typing import List

PUNCTUATION = ".,?\"'[]{};:<>/\\-=+|`~@#$%^&*()\n! "


def text_in_to_split_text(text_in: str) -> (List[str], bool):
    if len(text_in) == 0:
        return []

    split_text = [""]
    i = 0
    start_punctuation = text_in[0] in PUNCTUATION
    punctuation = start_punctuation
    for c in text_in:
        if (c in PUNCTUATION and punctuation) or (c not in PUNCTUATION and not punctuation):
            split_text[i] += c
        else:
            punctuation = not punctuation
            split_text.append(c)
            i += 1

    return split_text, start_punctuation


def TranslatePhonetic(text_in: str, db: Database) -> str:
    if len(text_in) == 0:
        return ""

    split_text, start_punctuation = text_in_to_split_text(text_in)

    out_str = ""

    retrieved_words = {}
    punctuation = start_punctuation
    for w in split_text:
        if punctuation:
            out_str += w
        else:
            if w in retrieved_words.keys():
                word = retrieved_words[w]
            else:
                try:
                    word = db.GetWord(w)
                    retrieved_words[w] = word
                except WordNotFoundError:
                    out_str += f"[{w} doesn't exist] "
                    punctuation = not punctuation
                    continue

            if word.phonetic_eng != "":
                out_str += word.phonetic_eng
            else:
                out_str += word.name

        punctuation = not punctuation

    return out_str


def TranslateAll(text_in: str, db: Database, mode: bool) -> str:
    translator = Translator(text_in, db, mode)

    string = ""

    while True:
        step = translator.step()
        translator.index += 1
        if step is None:
            break

        string += step.starting_punct

        if step.word_not_found:
            string += f"['{step.source_word}' not a word]"
        elif len(step.translation_options) == 1:
            string += step.translation_options[0]
        elif len(step.translation_options) > 1:
            string += "[" + "/".join(step.translation_options) + "]"
        else:
            string += f"[NT for '{step.source_word}']"

        string += step.trailing_punct

    return string


""" Old translate all
def TranslateAll(text_in: str, db: Database, mode: bool) -> str:
    if len(text_in) == 0:
        return ""

    split_text, start_punctuation = text_in_to_split_text(text_in)

    out_str = ""

    if mode:
        retrieved_words = {}

        punctuation = start_punctuation
        for w in split_text:
            if punctuation:
                out_str += w
            else:
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
            punctuation = not punctuation

    else:
        translations = {}
        for w in db.GetAllWords():
            for s in w.eng_synonyms:
                if s in translations.keys():
                    translations[s].append(w.name)
                else:
                    translations[s] = [w.name]

        punctuation = start_punctuation
        for w in split_text:
            if punctuation:
                out_str += w
            else:
                if w not in translations.keys():
                    out_str += f"[NT for {w}]"
                else:
                    trans = translations[w]
                    if len(trans) == 1:
                        out_str += trans[0]
                    else:
                        out_str += "[" + "/".join([x for x in trans]) + "]"
            punctuation = not punctuation

    return out_str
"""

@dataclass
class TranslationStep:
    translation_options: List[str]
    source_word: str
    word_not_found: bool
    current_word: int
    total_words: int
    mode: bool
    highlight_region: (int, int)
    starting_punct: str = ""
    trailing_punct: str = ""


class Translator:
    def __init__(self, text_in: str, db: Database, mode: bool):
        Log("TRNSLT", "Pre-processing translation")
        if len(text_in) == 0:
            text_in = "\n"

        self.split_text, self.start_punctuation = text_in_to_split_text(text_in)

        self.highlight_regions = []

        i = 0
        for j, sect in enumerate(self.split_text):
            if (j % 2 == 0 and self.start_punctuation) or (not j % 2 == 0 and not self.start_punctuation):
                i += len(sect) - 1
                continue
            self.highlight_regions.append((i, i + len(sect)))
            i += len(sect) + 1

        while True:
            try:
                pos = self.split_text.index("")
                self.split_text.pop(pos)
                self.highlight_regions.pop(pos)
            except ValueError:
                break
        self.db = db

        # self.db_all_words = None
        # self.translations = None
        # self.re_index()

        self.mode = mode

        if self.start_punctuation:
            self.index_offset = 1
        else:
            self.index_offset = 0
        self.index = 0

        Log("TRNSLT", "Pre-processing translation complete")

    # def re_index(self):
    #     self.db_all_words = self.db.GetAllWords()
    #
    #     self.translations = {}
    #     for word in self.db_all_words:
    #         for s in word.eng_synonyms:
    #             if s in self.translations.keys():
    #                 self.translations[s].append(word.name)
    #             else:
    #                 self.translations[s] = [word.name]

    def return_builder(self, options: List[str], w: str, highlight_region: (int, int),
                       word_not_found: bool = False) -> TranslationStep:

        starting_punct = ""
        trailing_punct = ""

        if self.start_punctuation:
            starting_punct = self.split_text[self.index * 2]
        else:
            trailing_punct = self.split_text[self.index * 2 + 1]

        return TranslationStep(options, w, word_not_found, self.index, len(self.split_text), self.mode,
                               highlight_region, starting_punct, trailing_punct)

    def step(self) -> TranslationStep | None:
        if (self.index * 2) + self.index_offset >= len(self.split_text):
            return None

        Log("TRNSLT", f"Translating step {(self.index * 2) + self.index_offset + 1}/{len(self.split_text)}")

        w = self.split_text[(self.index * 2) + self.index_offset]
        highlight = self.highlight_regions[self.index]

        if self.mode:
            try:
                self.db.GetWord(w)
            except WordNotFoundError:
                return self.return_builder([], w, highlight, True)

            trans = self.db.GetEngTrans(w)

            return self.return_builder(trans, w, highlight)
            # if len(word.eng_synonyms) == 0:
            #     return self.return_builder([], w)
            # elif len(word.eng_synonyms) == 1:
            #     return self.return_builder(word.eng_synonyms, w)
            # else:
            #     return self.return_builder(word.eng_synonyms, w)

        else:
            trans = self.db.GetLangTrans(w)

            return self.return_builder(trans, w, highlight)
