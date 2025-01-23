from tkinter import *
import customtkinter as ctk
import main


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


def open_popup():
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


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Project shortcuts")
root.geometry("500x500")

title_label = ctk.CTkLabel(root, text="Project shortcuts", font=("Arial", 20))
title_label.pack(pady=20)

add_button = ctk.CTkButton(root, text="Add Shortcut", command=open_popup)
add_button.pack(pady=20)

root.mainloop()