# -*- coding: utf-8 -*-
"""
A Python installer for Windows.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import os
import sys
from threading import Thread
import shutil
from ast import literal_eval

f_info = open("intall_info.txt", mode="r", encoding="UTF-8")
f_info_r = f_info.read()
f_info.close()

intall_info = literal_eval(f_info_r)

EXECUTABLE = intall_info["EXECUTABLE_NAME"]     # the executable file (*.exe)

TEXT_INSTALL = {        # set your text for installer
    "info":intall_info["INFO"],
    "license":intall_info["LICENCE"]
}

APP_NAME = intall_info["APP_NAME"]

APP_SIZE = intall_info["SIZE_MO"]

del intall_info

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

    T007 = {
        "fr":"Paramètres :",
        "en":"Setting:"
    }

    T008 = {
        "fr":"Ajouter au bureau",
        "en":"Add to desktop"
    }

    T009 = {
        "fr":"Ajouter au path",
        "en":"Add to path"
    }

    T010 = {
        "fr":"Dossier d'instalation :",
        "en":"Installation folder:"
    }

    T011 = {
        "fr":"📂 Ouvrir",
        "en":"📂 Open"
    }

    T012 = {
        "fr":"Erreur",
        "en":"Error"
    }

    T013 = {
        "fr":"Le chemain spécifier est vide.",
        "en":"The specified path is empty."
    }

    T014 = {
        "fr":"Instalation",
        "en":"Install"
    }

    T015 = {
        "fr":"Installation en cours,\nne fermer pas la fenêtre...",
        "en":"Insalling,\ndo not close the window..."
    }

    T016 = {
        "en":"Installation is complete.",
        "fr":"L'instalation est terminer."
    }



bool_agree = None
button_next_1 = None
add_desktop = None
add_path = None


path_copy = os.environ["LOCALAPPDATA"]

if hasattr(sys, "_MEIPASS"):
    data_path = os.path.join(sys._MEIPASS, "chemain relatif")

else:
    data_path = os.path.abspath("")

def step_3() -> None:
    """Configure the frame for step_3"""
    def install() -> None:
        """Copy all file."""
        nonlocal end_copy
        shutil.unpack_archive(os.path.join(data_path, "data.zip"), os.path.join(path_copy, APP_NAME))

        end_copy = True

    end_copy = False

    thread_copy = Thread(target=install, daemon=True)
    thread_copy.start()

    window_install.protocol("WM_DELETE_WINDOW", lambda: None)

    step[2].destroy()

    def while_install() -> None:
        """while the installation, controle if the intall have finish."""
        if end_copy:
            text_copy.destroy()

            text_end = tk.Label(step[3], text=Trad.T016[language])
            text_end.pack()

            try:
                tk.Label(step[3], text="✔️", fg="#00FF2F", font=("Segoe UI Emoji", 50)).pack()
            except:pass

        else:
            window_install.after(100, while_install)


    step[3].configure(text=Trad.T014[language])
    step[3].pack(fill="both", expand=True)

    text_copy = tk.Label(step[3], text=Trad.T015[language])
    text_copy.pack()

    while_install()



def step_2() -> None:
    """Configure the frame for step_2"""
    def start_next() -> None:
        """Call step_3."""
        path = entry_path.get()

        if path:
            global path_copy
            path_copy = path
            step_3()
        
        else:
            messagebox.showerror(Trad.T012[language], Trad.T013[language])

    def select_folder() -> None:
        """Set the the Entry for path the celected folder by user (with filedialog)."""
        path = filedialog.askdirectory(initialdir=path_copy)

        if path:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, path)


    global add_desktop, add_path
    step[1].destroy()

    step[2].configure(text=Trad.T007[language])
    step[2].pack(expand=True, fill="both")

    frame_config = tk.Frame(step[2])
    frame_config.grid(column=0, row=0)

    add_desktop = tk.BooleanVar(step[2], value=True)
    add_path = tk.BooleanVar(step[2], value=True)

    radio_add_desktop = tk.Checkbutton(frame_config, text=Trad.T008[language], variable=add_desktop)
    radio_add_desktop.pack(anchor="w")

    radio_add_path = tk.Checkbutton(frame_config, text=Trad.T009[language], variable=add_path)
    radio_add_path.pack(anchor="w")

    frame_path = tk.LabelFrame(frame_config, text=Trad.T010[language])
    frame_path.pack(anchor="w")

    entry_path = tk.Entry(frame_path, width=50)
    entry_path.insert(0, path_copy)
    entry_path.grid(column=0, row=0)

    button_open = tk.Button(frame_path, text=Trad.T011[language], command=select_folder)
    button_open.grid(column=1, row=0)

    button_next_2 = tk.Button(step[2], text=Trad.T003[language], command=start_next)
    button_next_2.grid(column=1, row=1, pady=50)



def step_1() -> None:
    """Configure the frame for step_1"""
    def start_next() -> None:
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

    button_next_1 = tk.Button(step[1], text=Trad.T003[language], command=start_next)
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
