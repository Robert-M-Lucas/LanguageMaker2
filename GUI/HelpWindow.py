from tkinter import *
from tkhtmlview import HTMLLabel
import os
from utils import ROOT_DIR


class HelpWindow:
    def __init__(self, top: Toplevel | Tk, filename: str):
        top.bind("<F1>", self.show_help)
        self.parent = top

        self.filename = filename

    def show_help(self, event):
        top = Toplevel(self.parent)
        top.title(self.filename)
        top.grab_set()

        with open(f"CACHE/CompiledHelpText/{self.filename}.md.html", "r") as f:
            frame = HTMLLabel(top, html=f.read())
        frame.pack(fill="both", expand=True)
