from tkinter import messagebox
from tkinter import *
from typing import List

from .InputPopup import InputPopup

from Translator import TranslateAll, Translator, TranslationStep, TranslatePhonetic
from Database import DatabaseExceptions
from .WordSelector import WordSelector


class MainGuiTranslation:
    def __init__(self):
        self.trans_top = None
        self.trans_top_root = None
        self.master = None
        self.translator = None
        self.database = None
        self.stepped = None
        self.text_in = None
        self.trans_text = None

    def translate_phonetic(self):
        self.trans_text.delete('1.0', END)
        self.trans_text.insert('1.0', TranslatePhonetic(self.text_in.get("1.0", END), self.database))

    def translate(self, mode: bool):
        self.trans_text.delete('1.0', END)
        if self.stepped.get() == 0:
            self.trans_text.insert('1.0', TranslateAll(self.text_in.get("1.0", END), self.database, mode))
        else:
            self.start_stepped_translate(mode)

    def start_stepped_translate(self, mode: bool):
        self.translator = Translator(self.text_in.get("1.0", END), self.database, mode)
        self.stepped_translate()

    def stepped_translate(self):
        step = self.translator.step()
        self.translator.index += 1

        if step is None:
            if self.trans_top is not None:
                self.end_stepped_translate()
            return

        if len(step.translation_options) == 1:
            self.trans_text.insert(END, step.translation_options[0] + " ")
            self.stepped_translate()
            return

        self.text_in.tag_delete("high")
        self.text_in.tag_add("high", f"1.0+ {step.highlight_region[0]} chars", f"1.0+ {step.highlight_region[1]} chars")
        self.text_in.tag_config("high", background="yellow")

        if self.trans_top is None:
            self.trans_top = Toplevel(self.master)
            self.trans_top.protocol("WM_DELETE_WINDOW", self.end_stepped_translate)

        self.trans_top.grab_set()

        self.trans_top.title(f"{step.source_word} synonym options")

        if self.trans_top_root is not None:
            self.trans_top_root.destroy()

        self.trans_top_root = Frame(self.trans_top)
        self.trans_top_root.pack()

        # try:
        #     self.database.GetWord(step.source_word)
        #     wordExists = True
        # except DatabaseExceptions.WordNotFoundError:
        #     wordExists = False

        if len(step.translation_options) > 0:
            Label(self.trans_top_root, text=f"Translation for {step.source_word}").pack(fill=X)

            lb_list = step.translation_options
            lb_var = StringVar(value=lb_list)
            lb = Listbox(self.trans_top_root, listvariable=lb_var)
            lb.select_set(0)
            lb.pack(fill=X)

            Button(self.trans_top_root, text="Add synonym", command=lambda:
            InputPopup(self.trans_top_root, self.add_syn_trans, f"Enter synonym for '{step.source_word}'", True, [step])
                   ).pack(fill=X)
            Button(self.trans_top_root, text="Select", command=lambda: self.insert_word_stepped(lb, lb_list)).pack(
                fill=X)

        elif step.word_not_found:
            Label(self.trans_top_root, text=f"'{step.source_word}' doesn't exist").pack(fill=X)
            Button(self.trans_top_root, text=f"Create '{step.source_word}' as new word",
                   command=lambda: self.create_stepped_word(step)).pack(fill=X)

            Button(self.trans_top_root, text=f"Skip this word",
                   command=lambda: self.skip_stepped_word(step)).pack(fill=X)

        elif step.mode:
            Label(self.trans_top_root,
                  text=f"No English translation for\n'{self.database.language}' word '{step.source_word}'").pack(fill=X)
            Button(self.trans_top_root, text="Add translation", command=lambda:
            InputPopup(self.trans_top_root, self.add_syn_trans, f"Enter translation for {step.source_word}", True,
                       [step])
                   ).pack(fill=X)
            Button(self.trans_top_root, text=f"Skip this word",
                   command=lambda: self.skip_stepped_word(step)).pack(fill=X)

        else:
            Label(self.trans_top_root,
                  text=f"No '{self.database.language}' translation for\nEnglish word '{step.source_word}'").pack(fill=X)
            Button(self.trans_top_root, text="Add translation", command=lambda:
            WordSelector(self, self.database.language, True, lambda word: self.add_syn_trans(word, step))).pack(fill=X)
            Button(self.trans_top_root, text=f"Skip this word",
                   command=lambda: self.skip_stepped_word(step)).pack(fill=X)

    def create_stepped_word(self, step: TranslationStep):
        self.database.AddWord(step.source_word)

        self.translator.index -= 1
        self.stepped_translate()

    def skip_stepped_word(self, step: TranslationStep):
        self.trans_text.insert(END, f"[NT for '{step.source_word}'] ")

        self.stepped_translate()

    def insert_word_stepped(self, lb: Listbox, lb_list: List[str]):
        self.trans_text.insert(END, lb_list[lb.curselection()[0]] + " ")

        self.stepped_translate()

    def end_stepped_translate(self):
        self.trans_top.destroy()
        self.text_in.tag_delete("high")
        self.trans_top = None

    def add_syn_trans(self, syn, step: TranslationStep):
        if step.mode:

            word = self.database.GetWord(step.source_word)
            word.eng_synonyms += [syn]

            self.database.UpdateWord(word)

            self.translator.index -= 1

            self.stepped_translate()
        else:
            try:
                word = self.database.GetWord(syn)
            except DatabaseExceptions.WordNotFoundError:
                messagebox.showerror(f"Word '{syn}' not found", f"Word '{syn}' wasn't found, use the Word Manager to "
                                                                f"create new words")
                self.translator.index -= 1
                self.stepped_translate()
                return

            word.eng_synonyms.append(step.source_word)

            self.database.UpdateWord(word)

            self.translator.index -= 1

            self.stepped_translate()
