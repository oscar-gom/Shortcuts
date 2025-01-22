import time
from pynput import keyboard
import csv
import os

# Test data
shortcuts = {
    "mpro": "correoprofesional@gmail.com ",
    "mpers": "correopersonal@gmail.com ",
    "ulinked": "https://www.linkedin.com/in/usuario ",
    "ugit": "github.com/usuario ",
    "prechazo": "Estimado [nombre] [apellido],\n\nLamentablemente, no podemos continuar con su solicitud de empleo. Agradecemos su interés en nuestra empresa y le deseamos éxito en sus futuros proyectos.\n\nAtentamente,\n[Nombre] [Apellido]\n[Posición] ",
}

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
                for _ in range(len(command) + 1) :
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

def main():
    # Create csv file
    if not os.path.exists("shortcuts.csv"):
        with open("shortcuts.csv", mode="w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Confirmation Key","Shortcut", "Text"])
            for key, value in shortcuts.items():
                writer.writerow([confirm_key ,key, value])
    else:
        print("File already exists")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()