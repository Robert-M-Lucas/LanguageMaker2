from tkinter import *
from Database.Database import Database
from .WordSelector import WordSelector
from .SynonymManager import SynonymManager
from .WordManager import WordManager
from Translator import TranslateAll, Translator, TranslationStep


class MainGui:
    def __init__(self, lang):
        self.database = Database(lang)

        self.master = Tk()
        self.master.title("Language Maker 2 - " + lang)
        self.root = Frame(self.master)
        self.root.pack()

        Button(self.root, text="Word Manager", command=lambda: WordSelector(self, lang)).pack(fill=X)

        self.mid_frame = Frame(self.root)
        self.mid_frame.pack()

        self.left = Frame(self.mid_frame)
        self.left.grid(row=0, column=0)
        self.right = Frame(self.mid_frame)
        self.right.grid(row=0, column=1)

        Label(self.left, text="Text in").pack()
        self.text_in = Text(self.left, width=40, height=15)
        self.text_in.pack()

        Label(self.right, text="Translated text").pack()
        self.trans_text = Text(self.right, width=40, height=15)
        self.trans_text.pack()

        Button(self.left, text=f"English to {lang}", command=lambda: self.translate(False)).pack(fill=X)

        self.right_bottom = Frame(self.right)
        self.right_bottom.pack(fill=X)
        Button(self.right_bottom, text=f"{lang} to English", command=lambda: self.translate(True), width=30).grid(row=0, column=0, sticky=N+E+S+W)
        self.deterministic = IntVar()
        Checkbutton(self.right_bottom, text="Deterministic", variable=self.deterministic, width=10).grid(row=0, column=1)

        self.translator = None
        self.trans_top = None
        self.trans_top_root = None

        self.master.mainloop()

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

        if step is None:
            if self.trans_top is not None:
                self.trans_top.destroy()
            else:
                self.trans_top = None
            return

        if self.trans_top is None:
            self.trans_top = Toplevel(self.master)
            self.trans_top.grab_set()

        self.trans_top.title(f"{step.source_word} synonym options")

        if self.trans_top_root is not None:
            self.trans_top_root.destroy()

        self.trans_top_root = Frame(self.trans_top)
        self.trans_top_root.pack()

        Label(self.trans_top_root, text=f"Translation for {step.source_word}").pack(fill=X)
        lb_var = StringVar(value=step.translation_options)
        lb = Listbox(self.trans_top_root, listvariable=lb_var)
        lb.select_set(0)
        lb.pack(fill=X)

        Button(self.trans_top_root, text="Add synonym").pack(fill=X)
        Button(self.trans_top_root, text="Select", command=self.stepped_translate).pack(fill=X)
