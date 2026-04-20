# -*- coding: utf-8 -*-
"""
A Python installer for Windows.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext

EXECUTABLE = ".exe"     # the executable file (*.exe)
FILES = ()              # other files (conf, icon, other *.exe...)

TEXT_INSTALL = {        # set your text for installer
    "info":"Information about app.",
    "license":"Information about license."
}

UPDATE_TIME = 100

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

    T003 = {
        "en":"Next",
        "fr":"Suivant"
    }

    T004 = {
        "en":"Licence:",
        "fr":"Licence :"
    }

    T005 = {
        "en":"Not agree",
        "fr":"Refuser"
    }

    T006 = {
        "en":"Agree",
        "fr":"Acepter"
    }


bool_agree = None
button_next_1 = None

def step_2() -> None:
    """Configure the frame for step_2"""
    step[1].destroy()

def step_1() -> None:
    """Configure the frame for step_1"""
    def start_nex() -> None:
        """Call step_2 if the user have agree licence."""
        if bool_agree.get():
            step_2()

    def set_button() -> None:
        """Set the state of button for agree licence."""
        try:
            button_next_1["state"] = "normal" if bool_agree.get() else "disabled"

            window_install.after(UPDATE_TIME, set_button)
        
        except:
            pass



    global bool_agree, button_next_1

    step[0].destroy()

    step[1].pack(expand=True, fill="both")
    step[1].configure(text=Trad.T004[language])

    license_text = scrolledtext.ScrolledText(step[1], height=7, width=50)
    license_text.grid(column=0, row=0, columnspan=2)
    license_text.insert(0.0, TEXT_INSTALL["license"])
    license_text["state"] = "disabled"

    frame_agree = tk.Frame(step[1])
    frame_agree.grid(column=0, row=1, sticky="w", pady=10)

    bool_agree = tk.BooleanVar(frame_agree, value=False)

    not_agree = tk.Radiobutton(frame_agree, text=Trad.T005[language], variable=bool_agree, value=False)
    not_agree.pack(anchor="w")

    agree = tk.Radiobutton(frame_agree, text=Trad.T006[language], variable=bool_agree, value=True)
    agree.pack(anchor="w")

    button_next_1 = tk.Button(step[1], text=Trad.T003[language], command=start_nex)
    button_next_1.grid(column=1, row=1)

    set_button()



if EXECUTABLE == "":
    messagebox.showerror(Trad.T000[language], Trad.T001[language])
    quit()

window_install = tk.Tk()
window_install.title(Trad.T002[language])

step = [tk.LabelFrame(window_install) for i in range(4)]

step[0].pack(expand=True, fill="both")

text_info = tk.Label(step[0], text=TEXT_INSTALL["info"])
text_info.grid(column=1, row=0, sticky="sewn")

button_next = tk.Button(step[0], text=Trad.T003[language], command=step_1)
button_next.grid(column=1, row=1, sticky="sewn")

window_install.geometry("430x200")
window_install.resizable(False, False)
window_install.mainloop()
