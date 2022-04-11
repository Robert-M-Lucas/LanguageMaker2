from tkinter import *
from tkhtmlview import HTMLLabel
import os

from logger import *
from utils import ROOT_DIR


class HelpWindow:
    def __init__(self, top: Toplevel | Tk, filename: str):
        top.bind("<F1>", self.show_help)
        self.parent = top

        self.filename = filename

    def show_help(self, event):
        top = Toplevel(self.parent)
        width = top.winfo_screenwidth()
        height = top.winfo_screenheight()
        top.geometry(f'{int(width/3)}x{int(height/2)}+{int((width/3)*2)}+0')
        top.title(self.filename)

        Log("HELPGUI", f"Loading help from: 'CACHE/CompiledHelpText/{self.filename}.md.html'")

        with open(f"CACHE/CompiledHelpText/{self.filename}.md.html", "r") as f:
            frame = HTMLLabel(top, html=f.read())

        frame.grid(sticky=N+E+S+W, row=0, column=0)

        sb = Scrollbar(top, command=frame.yview)
        frame.config(yscrollcommand=sb.set)
        sb.grid(sticky=N+E+S+W, row=0, column=1)

        Grid.columnconfigure(top, 0, weight=1)
        Grid.rowconfigure(top, 0, weight=1)
