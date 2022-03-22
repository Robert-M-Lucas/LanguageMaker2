from tkinter import *
from Translator import TranslateAll, Translator
from .InputPopup import InputPopup
from typing import List


class MainGuiTranslation:
    def translate(self, mode: bool):
        if self.deterministic.get() == 0:
            self.trans_text.delete('1.0', END)
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
                self.trans_top.destroy()
                self.trans_top = None
            return

        if self.trans_top is None:
            self.trans_top = Toplevel(self.master)
            self.trans_top.protocol("WM_DELETE_WINDOW", self.end_stepped_translate)
            self.trans_top.grab_set()

        self.trans_top.title(f"{step.source_word} synonym options")

        if self.trans_top_root is not None:
            self.trans_top_root.destroy()

        self.trans_top_root = Frame(self.trans_top)
        self.trans_top_root.pack()

        if len(step.translation_options) > 0:
            Label(self.trans_top_root, text=f"Translation for {step.source_word}").pack(fill=X)

            lb_list = step.translation_options
            lb_var = StringVar(value=lb_list)
            lb = Listbox(self.trans_top_root, listvariable=lb_var)
            lb.select_set(0)
            lb.pack(fill=X)

            Button(self.trans_top_root, text="Add synonym", command=lambda:
            InputPopup(self.trans_top_root, self.add_syn_trans, f"Enter synonym for {step.source_word}", True, [step])
                   ).pack(fill=X)
            Button(self.trans_top_root, text="Select", command=lambda: self.insert_word_stepped(lb, lb_list)).pack(fill=X)

        elif step.mode:
            Label(self.trans_top_root, text=f"No synonyms for {step.source_word}").pack(fill=X)
            Button(self.trans_top_root, text="Add synonym", command=lambda:
            InputPopup(self.trans_top_root, self.add_syn_trans, f"Enter synonym for {step.source_word}", True, [step])
                   ).pack(fill=X)
        else:
            Label(self.trans_top_root, text=f"No translation for {step.source_word}").pack(fill=X)
            Button(self.trans_top_root, text=f"Create new word (WIP)").pack(fill=X)

    def insert_word_stepped(self, lb: Listbox, lb_list: List[str]):
        self.trans_text.insert(END, lb_list[lb.curselection()[0]] + " ")

        self.stepped_translate()

    def end_stepped_translate(self):
        self.trans_top.destroy()
        self.trans_top = None

    def add_syn_trans(self, syn, step):
        word = self.database.GetWord(step.source_word)
        word.eng_synonyms += ";" + syn

        self.database.UpdateWord(word)

        self.translator.index -= 1
        self.translator.re_index()

        self.stepped_translate()
