# Shortcuts

Shortcuts is a Python-based application that allows users to create, save, and manage keyboard shortcuts for various commands and text snippets. The application uses a graphical user interface (GUI) built with the `customtkinter` library to provide an easy-to-use environment for managing shortcuts.

## Features

- Create and save keyboard shortcuts.
- Edit existing shortcuts.
- Customize application settings.
- User-friendly GUI with `customtkinter`.

## How to Generate an Executable

To create an executable file for the application, you can use the `pyinstaller` library. Follow the steps below:

1. Install `pyinstaller` if you haven't already:
   ```bash
   pip install pyinstaller
   ```

2. Navigate to the directory containing `ui.py`.

3. Run the following command to generate a standalone executable:
   ```bash
   pyinstaller --onefile --windowed ui.py
   ```

   - `--onefile`: Packages everything into a single executable file.
   - `--windowed`: Prevents a console window from appearing when the application is launched.

4. The executable file will be located in the `dist` directory.

---


If you want the exe without the effort: [Gumroad](https://oscargo.gumroad.com/l/shortcuts)
