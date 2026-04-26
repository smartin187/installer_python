# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, filedialog, ttk
except Exception as e:
    input(f"Installer is damaged.\nDetail: {str(e)}\nPress Enter for exit.")
    quit()

try:
    import os
    import sys
    from threading import Thread
    import shutil
    from ast import literal_eval
    from win32com.client import Dispatch
    import winreg
    from pathlib import Path
    import pythoncom
    import pywintypes
    import locale
    import ctypes
    import subprocess
except Exception as e:
    messagebox.showerror("Error", "Installer is damaged, impossible to load module.", detail=f"Detail: {str(e)}")
    quit()

def main() -> None:
    """
    A Python installer for Windows.
    """
    if hasattr(sys, "_MEIPASS"):
        data_path = os.path.abspath(sys._MEIPASS)

    else:
        data_path = os.path.abspath("")
    
    try:
        f_info = open(os.path.join(data_path, "install_info.txt"), mode="r", encoding="UTF-8")
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
    except Exception as e:
        messagebox.showerror("Error", "Error with file 'install_info.txt'", detail="Detail: " + str(e))
        quit()

    UPDATE_TIME = 100

    try:
        language = locale.getlocale()[0].split("_")[0]
    except:
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

        T017 = {
            "en":"Error",
            "fr":"Erreur"
        }

        T018 = {
            "en":"Impossible to create shortcut on desktop.",
            "fr":"Impossible de crée le racoursis au bureau."
        }

        T019 = {
            "en":"Detail: {}",
            "fr":"Détail : {}"
        }

        T020 = {
            "en":"Error",
            "fr":"Erreur"
        }

        T021 = {
            "en":"An error occurred while adding to Path.",
            "fr":"Une erreur est arrivé lors de l'ajout au Path."
        }

        T022 = {
            "en":"An error occurred during installation.",
            "fr":"Une erreur est survenu durant l'instalation."
        }

        T023 = {
            "en":"Open {}",
            "fr":"Ouvrir {}"
        }

    bool_agree = None
    button_next_1 = None
    add_desktop = None
    add_path = None


    path_copy = os.environ["LOCALAPPDATA"]



    def add_to_user_path(folder: str) -> None:
        folder = os.path.abspath(folder)

        access = winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Environment", 0, access) as key:
            try:
                current_path, reg_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path, reg_type = "", winreg.REG_EXPAND_SZ

            parts = [p for p in str(current_path).split(";") if p]
            normalized = {os.path.normcase(os.path.normpath(p)) for p in parts}
            folder_norm = os.path.normcase(os.path.normpath(folder))

            if folder_norm not in normalized:
                new_path = ";".join(parts + [folder]) if parts else folder
                winreg.SetValueEx(key, "Path", 0, reg_type, new_path)

        # Notifie Windows qu'une variable d'environnement a changé
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
        )


    def step_3() -> None:
        """Configure the frame for step_3"""
        def install() -> None:
            """Copy all file."""
            nonlocal end_copy, end_zip, install_error

            path = os.path.join(path_copy, APP_NAME)

            try:
                shutil.unpack_archive(os.path.join(data_path, "data.zip"), path)

                end_zip = True

                progress_var.set(90)

                if add_desktop.get():
                    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            
                    pythoncom.CoInitialize()

                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
                            desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
                            path_ink = Path(desktop_path)

                        
                        shell = Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortCut(os.path.join(path_ink, APP_NAME + ".lnk"))
                        shortcut.TargetPath = os.path.join(path, EXECUTABLE)
                        shortcut.Description = TEXT_INSTALL["info"]
                        shortcut.Save()
                    

                    except pywintypes.com_error as e:
                        window_install.after(0, lambda: messagebox.showerror(Trad.T017[language], Trad.T018[language], detail=Trad.T019[language].format(str(e))))

                    except:
                        window_install.after(0, lambda: messagebox.showerror(Trad.T017[language]))

                    finally:
                        pythoncom.CoUninitialize()
                
                progress_var.set(95)
                
                if add_path.get():
                    
                    try:
                        exe_dir = os.path.dirname(os.path.join(path, EXECUTABLE))
                        add_to_user_path(exe_dir)
                    except Exception as e:
                        window_install.after(0, lambda: messagebox.showerror(Trad.T020[language], Trad.T021[language], detail=Trad.T019[language].format(str(e))))

                progress_var.set(100)

                end_copy = True
            
            except Exception as e:
                messagebox.showerror(Trad.T020[language], Trad.T022[language], detail=Trad.T019[language].format(str(e)))
                install_error = True
                quit()

        end_copy = False
        end_zip = False
        install_error = False

        thread_copy = Thread(target=install, daemon=True)
        thread_copy.start()

        window_install.protocol("WM_DELETE_WINDOW", lambda: None)

        step[2].destroy()

        def while_install() -> None:
            """while the installation, controle if the intall have finish."""
            if install_error:
                quit()

            elif end_copy:
                text_copy.destroy()
                progress_bar.destroy()

                text_end = tk.Label(step[3], text=Trad.T016[language])
                text_end.pack()

                try:
                    tk.Label(step[3], text="✔️", fg="#00FF2F", font=("Segoe UI Emoji", 50)).pack()
                except:pass

                open_app_bool = tk.BooleanVar(step[3])

                open_app = tk.Checkbutton(step[3], text=Trad.T023[language].format(APP_NAME), variable=open_app_bool)
                open_app.pack(side="left")

                def close_install() -> None:
                    """Close the install window."""
                    if open_app_bool.get():
                        app_dir = os.path.join(path_copy, APP_NAME)

                        path = os.path.join(app_dir, EXECUTABLE)

                        subprocess.Popen([path], cwd=app_dir)

                    window_install.destroy()

                window_install.protocol("WM_DELETE_WINDOW", close_install)

                if install_error:
                    window_install.destroy()

            else:
                if not end_zip:
                    size = sum(f.stat().st_size for f in Path(abs_path).rglob('*') if f.is_file()) / 1048576
                    if not end_zip:     #double controle because end_zip is suppose to change
                        progress_var.set(size / size_for_progress_bar)

                window_install.after(20, while_install)

        size_for_progress_bar = APP_SIZE * 90

        step[3].configure(text=Trad.T014[language])
        step[3].pack(fill="both", expand=True)

        abs_path = os.path.join(path_copy, APP_NAME)

        text_copy = tk.Label(step[3], text=Trad.T015[language])
        text_copy.pack()

        progress_var = tk.IntVar(step[3])

        progress_bar = ttk.Progressbar(step[3], maximum=100, variable=progress_var, length=430)
        progress_bar.pack(pady=20)

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


        nonlocal add_desktop, add_path
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

    text_app_name = tk.Label(step[0], text=APP_NAME, font=("Arial", 50, "bold"))
    text_app_name.grid(column=1, row=0, sticky="sewn")

    try:
        heit_image = 125
        image = tk.PhotoImage(file=os.path.join(data_path, "icon.png"), height=heit_image, width=heit_image)
        image_label = tk.Label(step[0], image=image, height=heit_image, width=heit_image)
        image_label.grid(column=0, row=0, rowspan=3)
    except:
        pass


    text_info = tk.Label(step[0], text=TEXT_INSTALL["info"])
    text_info.grid(column=1, row=1, sticky="sewn")

    button_next = tk.Button(step[0], text=Trad.T003[language], command=step_1)
    button_next.grid(column=1, row=2, sticky="sewn")

    window_install.geometry("430x200")
    window_install.resizable(False, False)
    try:
        window_install.iconphoto(False, image)
    except:
        pass
    window_install.mainloop()

try:
    main()
except Exception as e:
    messagebox.showerror("Error", "Fatal error during the instalation.", detail=f"Detail: {str(e)}")