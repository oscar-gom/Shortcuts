#PROTOTYPE
# This is the main file for the prototype of the project. It will be used to test the functionality of the project.
from pynput import keyboard

shortcuts = {
    "@mpro": "correoprofesional@gmail.com",
    "@mpers": "correopersonal@gmail.com",
    "@ulinked": "https://www.linkedin.com/in/usuario",
    "@ugit": "github.com/usuario",
    "@prechazo": "Estimado [nombre] [apellido],\n\nLamentablemente, no podemos continuar con su solicitud de empleo. Agradecemos su interés en nuestra empresa y le deseamos éxito en sus futuros proyectos.\n\nAtentamente,\n[Nombre] [Apellido]\n[Posición]",
}

reading = False
command = ""

def on_press(key):
    global reading
    global command
    try:
        if key == keyboard.Key.esc:
            reading = False
            command = ""
            print("Stop reading")
        elif hasattr(key, 'char') and key.char == "@":
            reading = True
            command += "@"
        elif key == keyboard.Key.backspace and reading:
            command = command[:-1]
            if command == "":
                reading = False
        elif hasattr(key, 'char') and reading:
            command += key.char
            print(command)
            if len(command) > 15:
                print("Command not found")
                reading = False
                command = ""
            elif command in shortcuts:
                print("Command found")
                print(shortcuts[command])
                reading = False
                command = ""
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()