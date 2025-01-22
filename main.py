import time
from pynput import keyboard
import csv
import os

# Test data
shortcuts = {}

reading = False
command = ""
controller = keyboard.Controller()
confirm_key = keyboard.Key.space


def on_press(key):
    global reading
    global command
    try:
        # Stops reading commands
        if key == keyboard.Key.esc:
            reading = False
            command = ""
            print("Stop reading")

        # User is typing a command
        elif hasattr(key, 'char') and any(key.char == k[0] for k in shortcuts.keys()):
            command += key.char
            reading = True

        # Deletes the last character of the command
        elif key == keyboard.Key.backspace and reading:
            command = command[:-1]
            if command == "":
                reading = False

        # Adds the character to the command
        elif hasattr(key, 'char') and reading:
            command += key.char
            print(command)

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
    with open("shortcuts.csv", mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key, key, value])


def load_shortcuts():
    global confirm_key

    with open("shortcuts.csv", mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != "Confirmation Key":
                shortcuts[row[1]] = row[2]
            else:
                confirm_key = row[1]


def add_shortcut(shortcut, text):
    shortcuts[shortcut] = text
    with open("shortcuts.csv", mode="a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([confirm_key, shortcut, text])


def update_shortcut(shortcut, text):
    shortcuts[shortcut] = text
    with open("shortcuts.csv", mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key, key, value])

    load_shortcuts()


def delete_shortcut(shortcut):
    del shortcuts[shortcut]
    with open("shortcuts.csv", mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key, key, value])

    load_shortcuts()


def get_shortcuts():
    return shortcuts


def get_confirm_key():
    return confirm_key


def set_confirm_key(key):
    global confirm_key
    confirm_key = key
    with open("shortcuts.csv", mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Confirmation Key", "Shortcut", "Text"])
        for key, value in shortcuts.items():
            writer.writerow([confirm_key, key, value])

    load_shortcuts()


def main():
    # Check if the csv exists
    if not os.path.exists("shortcuts.csv"):
        create_csv()
    else:
        load_shortcuts()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
