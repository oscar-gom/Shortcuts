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

# Read keyboard input
def on_press(key):
    try:
        if key.char == '@':
            print("Start reading")
    except AttributeError:
        pass


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()