from tkinter import *
from tkinter import messagebox

"""
This is meant to replicate an error with the MainGui - After a message box shows up focus is set to the main window,
not the top which has grab_set() allowing users to type in fields where they're not supposed to be able. This code
manages to demonstrate that this issue doesn't exist
"""


def show_error():
    global top
    messagebox.showerror("A", "B")
    top.grab_set()


def show_top():
    global top
    top = Toplevel(main)
    top.grab_set()
    Button(top, text="Error", command=show_error).pack()


top = None

main = Tk()
str_var = StringVar()
str_var.set("Don't type here")
Entry(main, textvariable=str_var).pack()
Button(top, text="Show top", command=show_top).pack()

main.mainloop()