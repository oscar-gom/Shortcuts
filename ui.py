from tkinter import *
import customtkinter as ctk
import main
import threading


def save_shortcut(entry_key, entry_shortcut):
    key = entry_key.get()
    shortcut = entry_shortcut.get()

    if not key or not shortcut:
        print("Both fields are required")
    else:
        print("Saving shortcut")
        main.add_shortcut(key, shortcut)
        entry_key.delete(0, END)
        entry_shortcut.delete(0, END)


def add_shortcut_popup():
    popup = ctk.CTkToplevel()
    popup.title("Add shortcut")
    popup.geometry("300x300")

    label_key = ctk.CTkLabel(popup, text="Insert the command:")
    label_key.pack(pady=10)

    entry_key = ctk.CTkEntry(popup)
    entry_key.pack(pady=10)

    label_shortcut = ctk.CTkLabel(popup, text="Insert the text:")
    label_shortcut.pack(pady=10)

    entry_shortcut = ctk.CTkEntry(popup)
    entry_shortcut.pack(pady=10)

    button = ctk.CTkButton(popup, text="Save", command=lambda: save_shortcut(entry_key, entry_shortcut))
    button.pack(pady=10)

    popup.mainloop()


def main_ui():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Project shortcuts")
    root.geometry("500x500")
    root.resizable(False, False)

    title_label = ctk.CTkLabel(root, text="Project shortcuts", font=("Arial", 20))
    title_label.pack(pady=20)

    # Initial check of csv file
    initial_check_thread = threading.Thread(target=main.initial_check)
    initial_check_thread.start()

    # Choose confirm key
    confirm_key_label = ctk.CTkLabel(root, text="Choose the confirm key:")
    confirm_key_label.pack(pady=10)

    options = ["Tab", "Space", "Enter"]
    confirm_key_default = main.get_confirm_key()
    confirm_key_selector = ctk.CTkOptionMenu(root, values=options)

    # If there are shortcuts, the confirm_key is displayed
    if main.shortcuts != {}:
        confirm_key_selector.set(confirm_key_default)

    confirm_key_selector.pack(pady=10)

    save_confirm_btn = ctk.CTkButton(root, text="Save confirm key",
                                     command=lambda: main.set_confirm_key(confirm_key_selector.get()))
    save_confirm_btn.pack(pady=10)

    add_button = ctk.CTkButton(root, text="Add Shortcut", command=add_shortcut_popup)
    add_button.pack(pady=30)

    # Add horizontal divider
    divider = ctk.CTkFrame(root, height=2, width=400)
    divider.pack(pady=10)

    # Show shortcuts
    shortcuts = main.get_shortcuts()
    for key, value in shortcuts.items():
        shortcut_frame = ctk.CTkFrame(root)
        shortcut_frame.pack(pady=10, fill="x", padx=50)

        key_label = ctk.CTkLabel(shortcut_frame, text=f"{key}: {value}")
        key_label.pack(side="left", padx=10)

        edit_button = ctk.CTkButton(shortcut_frame, text="Edit", command=lambda k=key, v=value: edit_shortcut_popup(k, v))
        edit_button.pack(side="right")

    root.mainloop()


if __name__ == "__main__":
    main_ui()
