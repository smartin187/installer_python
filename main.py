# -*- coding: utf-8 -*-
"""
A Python installer for Windows.
"""

import tkinter as tk
from tkinter import messagebox

EXECUTABLE = ".exe"     # the executable file (*.exe)
FILES = ()              # other files (conf, icon, other *.exe...)

TEXT_INSTALL = {        # set your text for installer
    "info":"Information about app."
}

language = "en"

class Trad:
    """The translate"""
    T000 = {
        "en":"Error",
        "fr":"Erreur"
    }

    T001 = {
        "en":"The installer is damaged...",
        "fr":"L'instalateur est endomagé..."
    }

    T002 = {
        "en":"Installer",
        "fr":"Instalateur"
    }

if EXECUTABLE == "":
    messagebox.showerror(Trad.T000[language], Trad.T001[language])
    quit()

window_install = tk.Tk()
window_install.title(Trad.T002[language])

text_info = tk.Label(window_install, text=TEXT_INSTALL["info"])
text_info.pack()



window_install.mainloop()
