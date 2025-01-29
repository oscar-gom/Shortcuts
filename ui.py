from tkinter import *
import customtkinter as ctk
import main
import threading


def save_shortcut(entry_key, entry_shortcut, root, message_label):
    key = entry_key.get()
    shortcut = entry_shortcut.get()

    if not key or not shortcut:
        if message_label.winfo_exists():
            message_label.configure(text="Both fields are required", text_color="red")
    else:
        try:
            main.add_shortcut(key, shortcut)
            entry_key.delete(0, END)
            entry_shortcut.delete(0, END)
            update_shortcut_list(root)
            if message_label.winfo_exists():
                message_label.configure(text="Shortcut saved successfully", text_color="green")
        except Exception as e:
            if message_label.winfo_exists():
                message_label.configure(text=f"Error: {str(e)}", text_color="red")


def add_shortcut_popup(root):
    popup = ctk.CTkToplevel()
    popup.title("Add shortcut")
    popup.geometry("300x300")

    label_key = ctk.CTkLabel(popup, text="Insert the command:", font=("Arial", 14))
    label_key.pack(pady=10)

    entry_key = ctk.CTkEntry(popup, width=250)
    entry_key.pack(pady=10)

    label_shortcut = ctk.CTkLabel(popup, text="Insert the text:", font=("Arial", 14))
    label_shortcut.pack(pady=10)

    entry_shortcut = ctk.CTkEntry(popup, width=250)
    entry_shortcut.pack(pady=10)

    message_label = ctk.CTkLabel(popup, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    button = ctk.CTkButton(popup, text="Save", command=lambda: save_shortcut(entry_key, entry_shortcut, root, message_label))
    button.pack(pady=20)

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
    pop_up.geometry("300x300")

    label_key = ctk.CTkLabel(pop_up, text="Command:", font=("Arial", 14))
    label_key.pack(pady=10)

    entry_key = ctk.CTkEntry(pop_up, width=250)
    entry_key.insert(0, k)
    entry_key.pack(pady=10)

    label_shortcut = ctk.CTkLabel(pop_up, text="Text:", font=("Arial", 14))
    label_shortcut.pack(pady=10)

    entry_shortcut = ctk.CTkEntry(pop_up, width=250)
    entry_shortcut.insert(0, v)
    entry_shortcut.pack(pady=10)

    message_label = ctk.CTkLabel(pop_up, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    button = ctk.CTkButton(pop_up, text="Save",
                           command=lambda: update_shortcut(entry_key.get(), entry_shortcut.get(), root, message_label))
    button.pack(pady=20)

    pop_up.mainloop()


def main_ui():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Project shortcuts")
    root.geometry("500x600")
    root.resizable(False, False)

    # Create a frame to hold the title and button
    top_frame = ctk.CTkFrame(root)
    top_frame.pack(side="top", fill="x", pady=10, padx=10)

    title_label = ctk.CTkLabel(top_frame, text="Project shortcuts", font=("Arial", 24, "bold"))
    title_label.pack(side="left", padx=10)

    add_button = ctk.CTkButton(top_frame, text="Add Shortcut", command=lambda: add_shortcut_popup(root=root))
    add_button.pack(side="right", padx=10)

    # Initial check of csv file
    initial_check_thread = threading.Thread(target=main.initial_check)
    initial_check_thread.start()

    # Create a frame to hold the confirm_key label, selector, and save button
    confirm_key_frame = ctk.CTkFrame(root)
    confirm_key_frame.pack(pady=10, padx=10, fill="x")

    confirm_key_label = ctk.CTkLabel(confirm_key_frame, text="Choose the confirm key:", font=("Arial", 14))
    confirm_key_label.pack(side="left", padx=10)

    options = ["Tab", "Space", "Enter"]
    confirm_key_default = main.get_confirm_key()
    confirm_key_var = ctk.StringVar(value=confirm_key_default)
    confirm_key_selector = ctk.CTkOptionMenu(confirm_key_frame, values=options, variable=confirm_key_var)
    confirm_key_selector.pack(side="left", padx=10)

    save_confirm_btn = ctk.CTkButton(confirm_key_frame, text="Save confirm key",
                                     command=lambda: save_confirm_key(confirm_key_selector.get(), save_confirm_btn))
    save_confirm_btn.pack(side="right", padx=10)

    # Disable the save button initially
    save_confirm_btn.configure(state="disabled")

    # Function to enable the save button when the confirm key changes
    def on_confirm_key_change(*args):
        if confirm_key_var.get() != confirm_key_default:
            save_confirm_btn.configure(state="normal")
        else:
            save_confirm_btn.configure(state="disabled")

    # Trace changes to the confirm_key variable
    confirm_key_var.trace_add("write", on_confirm_key_change)

    # Add horizontal divider
    divider = ctk.CTkFrame(root, height=2, width=400)
    divider.pack(pady=10)

    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(root, width=480, height=400)
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
        shortcut_frame = ctk.CTkFrame(frame)
        shortcut_frame.pack(pady=10, fill="x", padx=20)

        key_label = ctk.CTkLabel(shortcut_frame, text=f"{key}: {value}", font=("Arial", 12))
        key_label.pack(side="left", padx=10)

        edit_button = ctk.CTkButton(shortcut_frame, text="Edit",
                                    command=lambda k=key, v=value: edit_shortcut_popup(k, v, root=frame))
        edit_button.pack(side="right", padx=10)


if __name__ == "__main__":
    main_ui()
