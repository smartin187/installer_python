# Python Installer

This repository lets you build your own custom installer.

The installer itself is written in Python, but you can use it for any programming language—as long as you have a Windows executable (`*.exe`).

This installer is intentionally simple: it lets you create an installer quickly and easily, but it does not support advanced tasks such as creating custom keys in the Windows Registry.

## How to build the installer

You need [PyInstaller](https://pyinstaller.org/en/stable/) to compile the installer. You can install it with `pip`:
`pip install -U pyinstaller`

### Create the data files

The installer requires configuration files and data files (your application).

#### File `install_info.txt`

Create a file with the following format:
```install_info
{
    "APP_NAME":"Name of app",
    "EXECUTABLE_NAME":"myapp.exe",
    "INFO":"Information about app",
    "LICENCE":"Information about licence",
    "COMMAND":"",
    "SIZE_MO":10.0
}
```

The `COMMAND` key lets you run a command (in the Windows terminal) at the end of the installation. You can use it for custom actions.
The `SIZE_MO` key must contain the size of your application.

#### File `data.zip`

This file contains your entire application: your executable, additional configuration files, images, etc.

Use relative paths to access files from your executable.

#### File `icon.png`

_Optional_

You can add an icon to your installer. The required dimensions are `125x125`.

### Build the executable

In a terminal, run the following command:
```
pyinstaller main.py --onefile --add-data install_info.txt:. --add-data data.zip:. --add-data icon.png:.
```

(Add `--add-data icon.png:.` only if you have an icon.)

If the build succeeds, the output will be in the `dist` folder.

## Test without compiling

You can test the installer without compiling it.

To do so, create the same files as for compilation, then run the Python program directly:
```
python main.py
```

