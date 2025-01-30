import time
from pynput import keyboard
import csv
import os
import threading

shortcuts = {}

reading = False
command = ""
controller = keyboard.Controller()
confirm_key = keyboard.Key.space
timer = None

# User settings
delete_command_after_time = True
delete_command_time = 5


# Function to reset the timer
def reset_timer():
    global timer
    if delete_command_after_time:
        if timer:
            timer.cancel()
        timer = threading.Timer(delete_command_time, clear_command)
        timer.start()


# Function to clear the command
def clear_command():
    global command, reading
    command = ""
    reading = False
    print("Command cleared")


def on_press(key):
    global reading, command
    try:
        # Stops reading commands
        if key == keyboard.Key.esc:
            reading = False
            command = ""
            print("Stop reading")


        # Stops reading commands if the user presses enter, space, or tab and the confirm_key is not the same
        if key == keyboard.Key.enter and confirm_key != keyboard.Key.enter:
            clear_command()

        if key == keyboard.Key.space and confirm_key != keyboard.Key.space:
            clear_command()

        if key == keyboard.Key.tab and confirm_key != keyboard.Key.tab:
            clear_command()


        # User is typing a command
        elif hasattr(key, 'char') and any(key.char == k[0] for k in shortcuts.keys()):
            command += key.char
            reading = True
            reset_timer()  # Reset the timer

        # Deletes the last character of the command
        elif key == keyboard.Key.backspace and reading:
            command = command[:-1]
            if command == "":
                reading = False
            reset_timer()  # Reset the timer

        # Adds the character to the command
        elif hasattr(key, 'char') and reading:
            command += key.char
            print(command)
            reset_timer()  # Reset the timer

            # Command is too long
            if len(command) > 15:
                print("Command not found")
                reading = False
                command = ""

        # Command is found
        if key == confirm_key and reading:
            if command in shortcuts:
                print("Command found")
                print(shortcuts[command])

                # Delete command
                for _ in range(len(command) + 1):
                    controller.press(keyboard.Key.backspace)
                    controller.release(keyboard.Key.backspace)
                    time.sleep(0.05)

                # Type the result
                time.sleep(0.1)
                controller.type(shortcuts[command])

                command = ""
                reading = False
            else:
                print("Command not found")
                reading = False
                command = ""

    except AttributeError:
        pass


def create_csv():
    with open("shortcuts.csv", mode="w", encoding="utf-8", newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])


def load_shortcuts():
    global confirm_key

    with open("shortcuts.csv", mode="r", encoding="utf-8", newline='\n') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line
        for row in reader:
            shortcuts[row[1]] = row[2]

        key_text = row[0]
        if key_text == "Tab":
            confirm_key = keyboard.Key.tab
        elif key_text == "Space":
            confirm_key = keyboard.Key.space
        else:
            confirm_key = keyboard.Key.enter


def add_shortcut(shortcut, text):
    if not os.path.exists("shortcuts.csv"):
        create_csv()
    shortcuts[shortcut] = text
    with open("shortcuts.csv", mode="a", encoding="utf-8", newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([confirm_key.name.capitalize(), shortcut, text])


def update_shortcut(shortcut, text):
    shortcuts[shortcut] = text
    with open("shortcuts.csv", mode="w", encoding="utf-8", newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key.name.capitalize(), key, value])

    load_shortcuts()


def delete_shortcut(shortcut):
    del shortcuts[shortcut]
    with open("shortcuts.csv", mode="w", encoding="utf-8", newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key, key, value])

    load_shortcuts()


def get_shortcuts():
    return shortcuts


def get_confirm_key():
    return confirm_key.name.capitalize()


def set_confirm_key(key):
    global confirm_key

    if key == "Tab":
        confirm_key = keyboard.Key.tab
    elif key == "Space":
        confirm_key = keyboard.Key.space
    else:
        confirm_key = keyboard.Key.enter

    if shortcuts:
        with open("shortcuts.csv", mode="r", encoding="utf-8", newline='\n') as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open("shortcuts.csv", mode="w", encoding="utf-8", newline='\n') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[0] == "Confirmation Key":
                    writer.writerow(row)
                else:
                    row[0] = confirm_key.name.capitalize()
                    writer.writerow(row)

        load_shortcuts()


def initial_check():
    # Check if the csv exists
    if os.path.exists("shortcuts.csv"):
        print("File already")
        load_shortcuts()
        print(shortcuts)

    print(confirm_key, "confirm key")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
