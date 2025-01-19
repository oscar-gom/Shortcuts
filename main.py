#PROTOTYPE
# This is the main file for the prototype of the project. It will be used to test the functionality of the project.
import time

from pynput import keyboard

# Test data
shortcuts = {
    "mpro": "correoprofesional@gmail.com",
    "mpers": "correopersonal@gmail.com",
    "ulinked": "https://www.linkedin.com/in/usuario",
    "ugit": "github.com/usuario",
    "prechazo": "Estimado [nombre] [apellido],\n\nLamentablemente, no podemos continuar con su solicitud de empleo. Agradecemos su interés en nuestra empresa y le deseamos éxito en sus futuros proyectos.\n\nAtentamente,\n[Nombre] [Apellido]\n[Posición]",
}

reading = False
command = ""
trigger = "º"
controller = keyboard.Controller()

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
        elif hasattr(key, 'char') and key.char == trigger:
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
            elif command in shortcuts:
                print("Command found")
                print(shortcuts[command])

                # Type result
                for i in range(len(command)):
                    controller.press(keyboard.Key.backspace)
                    controller.release(keyboard.Key.backspace)

                #Delete command trigger
                for i in range(len(trigger)):
                    controller.press(keyboard.Key.backspace)
                    controller.release(keyboard.Key.backspace)

                controller.type(shortcuts[command])

                reading = False
                command = ""

    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()