import threading
from tkinter import *

import customtkinter as ctk
from customtkinter import CTkTextbox

import main


def save_all_settings(confirm_key, delete_time, enable_delete_time, message_label):
    main.set_confirm_key(confirm_key)
    main.set_delete_command_time(int(delete_time))
    main.set_delete_command_after_time(enable_delete_time)
    message_label.configure(text="Settings saved successfully", text_color="green")


def toggle_settings(enable, entry):
    if enable:
        entry.configure(state="normal")
    else:
        entry.configure(state="disabled")


def open_settings_popup():
    settings_popup = ctk.CTkToplevel()

    settings_popup.title("Settings")
    settings_popup.geometry("500x500")
    settings_popup.resizable(False, False)

    label = ctk.CTkLabel(settings_popup, text="Settings", font=("Arial", 14))
    label.pack(pady=20)

    # Create a frame to hold the confirm_key label and selector
    confirm_key_frame = ctk.CTkFrame(settings_popup, fg_color=settings_popup.cget("fg_color"))
    confirm_key_frame.pack(pady=10, padx=10, fill="x")

    confirm_key_label = ctk.CTkLabel(confirm_key_frame, text="Choose the confirm key:", font=("Arial", 14))
    confirm_key_label.pack(side="left", padx=(0, 20))

    options = ["Tab", "Space", "Enter"]
    confirm_key_default = main.get_confirm_key()
    confirm_key_var = ctk.StringVar(value=confirm_key_default)

    confirm_key_selector = ctk.CTkOptionMenu(confirm_key_frame, values=options, variable=confirm_key_var)
    confirm_key_selector.pack(side="left")

    # Create a checkbox to enable/disable the settings
    enable_settings_var = ctk.BooleanVar(value=main.delete_command_after_time)
    enable_settings_checkbox = ctk.CTkCheckBox(settings_popup, text="Enable command time settings",
                                               variable=enable_settings_var,
                                               command=lambda: toggle_settings(enable_settings_var.get(),
                                                                               delete_command_after_time_entry))
    enable_settings_checkbox.pack(pady=10)

    delete_command_after_time_frame = ctk.CTkFrame(settings_popup, fg_color=settings_popup.cget("fg_color"))
    delete_command_after_time_frame.pack(pady=10, padx=10, fill="x")

    delete_command_after_time_label = ctk.CTkLabel(delete_command_after_time_frame,
                                                   text="Delete command after (seconds):",
                                                   font=("Arial", 14))
    delete_command_after_time_label.pack(side="left", padx=(0, 20))

    delete_command_after_time_var = ctk.StringVar(value=str(main.delete_command_time))
    delete_command_after_time_entry = ctk.CTkEntry(delete_command_after_time_frame,
                                                   textvariable=delete_command_after_time_var)
    delete_command_after_time_entry.pack(side="left", padx=(0, 20))

    # Add a button to save all settings
    save_all_button = ctk.CTkButton(settings_popup, text="Save All",
                                    command=lambda: save_all_settings(confirm_key_selector.get(),
                                                                      delete_command_after_time_var.get(),
                                                                      enable_settings_var.get(),
                                                                      message_label))
    save_all_button.pack(pady=20)

    # Add a label to show the success message
    message_label = ctk.CTkLabel(settings_popup, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    # Author info:
    author_label = ctk.CTkLabel(settings_popup,
                                text="Thanks for downloading!\nIf you want to check me out or hire me you can find me here:",
                                font=("Arial", 14))
    author_label.pack(pady=(20, 10))

    linkedin_url = ctk.CTkLabel(settings_popup, text="https://www.linkedin.com/in/oscar-gomez-sedas/",
                                font=("Arial", 14))
    linkedin_url.pack(pady=(0, 5))

    github_url = ctk.CTkLabel(settings_popup, text="https://github.com/oscar-gom", font=("Arial", 14))
    github_url.pack(pady=(0, 5))

    # Ensure the popup is on top
    settings_popup.lift()
    settings_popup.grab_set()
    settings_popup.mainloop()


def save_shortcut(entry_key, entry_shortcut, root, message_label):
    key = entry_key.get()
    shortcut = entry_shortcut.get("1.0", "end-1c")  # Get text from the Textbox

    if not key or not shortcut:
        if message_label.winfo_exists():
            message_label.configure(text="Both fields are required", text_color="red")
    else:
        try:
            main.add_shortcut(key, shortcut)
            entry_key.delete(0, END)
            entry_shortcut.delete("1.0", END)
            update_shortcut_list(root)
            if message_label.winfo_exists():
                message_label.configure(text="Shortcut saved successfully", text_color="green")
        except Exception as e:
            if message_label.winfo_exists():
                message_label.configure(text=f"Error: {str(e)}", text_color="red")


def add_shortcut_popup(root):
    popup = ctk.CTkToplevel()
    popup.title("Add shortcut")
    popup.geometry("450x500")
    popup.resizable(False, False)

    label_key = ctk.CTkLabel(popup, text="Insert the command:", font=("Arial", 14))
    label_key.pack(pady=10)

    entry_key = ctk.CTkEntry(popup, width=250)
    entry_key.pack(pady=10)

    label_shortcut = ctk.CTkLabel(popup, text="Insert the text:", font=("Arial", 14))
    label_shortcut.pack(pady=10)

    entry_shortcut = ctk.CTkTextbox(popup, width=250)
    entry_shortcut.insert("1.0", "")
    entry_shortcut.pack(pady=10, padx=10, fill="both", expand=False)

    message_label = ctk.CTkLabel(popup, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    button = ctk.CTkButton(popup, text="Save",
                           command=lambda: save_shortcut(entry_key, entry_shortcut, root, message_label))
    button.pack(pady=20)

    # Ensure the popup is on top
    popup.lift()
    popup.grab_set()
    popup.mainloop()


def update_shortcut(entry, text, root, message_label):
    if not entry or not text:
        message_label.configure(text="Both fields are required", text_color="red")
    else:
        try:
            main.update_shortcut(entry, text)
            update_shortcut_list(root)
            message_label.configure(text="Shortcut updated successfully", text_color="green")
        except Exception as e:
            message_label.configure(text=f"Error: {str(e)}", text_color="red")


def edit_shortcut_popup(k, v, root):
    pop_up = ctk.CTkToplevel()
    pop_up.title("Edit shortcut")
    pop_up.geometry("450x500")
    pop_up.resizable(False, False)

    label_key = ctk.CTkLabel(pop_up, text="Command:", font=("Arial", 14))
    label_key.pack(pady=10)

    entry_key = ctk.CTkEntry(pop_up)
    entry_key.insert(0, k)
    entry_key.pack(pady=10)

    label_shortcut = ctk.CTkLabel(pop_up, text="Text:", font=("Arial", 14))
    label_shortcut.pack(pady=10)

    text_shortcut = CTkTextbox(pop_up, wrap="word")
    text_shortcut.insert("1.0", v)
    text_shortcut.pack(pady=10, padx=10, fill="both", expand=False)

    message_label = ctk.CTkLabel(pop_up, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    button = ctk.CTkButton(pop_up, text="Save",
                           command=lambda: update_shortcut(entry_key.get(), text_shortcut.get("1.0", "end-1c"), root,
                                                           message_label))
    button.pack(pady=20)

    # Ensure the popup is on top
    pop_up.lift()
    pop_up.grab_set()
    pop_up.mainloop()


def main_ui():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Project shortcuts")
    root.geometry("500x600")
    root.resizable(False, False)

    # Get the background color of the root window
    bg_color = root.cget("fg_color")

    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(root, width=480, height=400)

    # Create a frame to hold the settings button
    settings_frame = ctk.CTkFrame(root, fg_color=bg_color)
    settings_frame.pack(side="top", fill="x", pady=10, padx=10)

    settings_button = ctk.CTkButton(settings_frame, text="Settings", command=open_settings_popup)
    settings_button.pack(side="right")

    # Create a frame to hold the title and buttons
    top_frame = ctk.CTkFrame(root, fg_color=bg_color)
    top_frame.pack(side="top", fill="x", pady=10, padx=10)

    title_label = ctk.CTkLabel(top_frame, text="Project shortcuts", font=("Arial", 24, "bold"))
    title_label.pack(side="left")

    add_button = ctk.CTkButton(top_frame, text="Add Shortcut",
                               command=lambda: add_shortcut_popup(root=scrollable_frame))
    add_button.pack(side="right")

    # Initial check of csv file
    initial_check_thread = threading.Thread(target=main.initial_check)
    initial_check_thread.start()

    # Add horizontal divider
    divider = ctk.CTkFrame(root, height=2, width=400)
    divider.pack(pady=10)

    # Pack the scrollable frame
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    update_shortcut_list(scrollable_frame)

    root.mainloop()


def save_confirm_key(key, button):
    main.set_confirm_key(key)
    button.configure(state="disabled")


def update_shortcut_list(frame):
    # Clear previous shortcuts
    for widget in frame.winfo_children():
        widget.destroy()

    # Show shortcuts
    shortcuts = main.get_shortcuts()
    for key, value in shortcuts.items():
        # Replace newlines with spaces
        value_single_line = value.replace("\n", " ")
        # Truncate the value if it is too long
        display_value = value_single_line if len(value_single_line) <= 30 else value_single_line[:27] + "..."

        shortcut_frame = ctk.CTkFrame(frame)
        shortcut_frame.pack(pady=10, fill="x", padx=20)

        key_label = ctk.CTkLabel(shortcut_frame, text=f"{key}: {display_value}", font=("Arial", 12))
        key_label.pack(side="left", padx=10)

        edit_button = ctk.CTkButton(shortcut_frame, text="Edit",
                                    command=lambda k=key, v=value: edit_shortcut_popup(k, v, root=frame))
        edit_button.pack(side="right", padx=10)


if __name__ == "__main__":
    main_ui()
