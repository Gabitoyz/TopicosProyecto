# Importa ttkbootstrap para estilos modernos y tkinter para GUI
import ttkbootstrap as ttk
import tkinter as tk

# Define una clase que representa la vista de login (inicio de sesión)
class LoginView(ttk.Frame):
    # Constructor: recibe el contenedor padre y un callback para manejar el login
    def __init__(self, parent, login_callback):
        super().__init__(parent, padding=20)  # Inicializa el frame con padding
        self.pack(fill="both", expand=True)   # Hace que el frame se expanda y llene el espacio
        self.login_callback = login_callback  # Guarda la función a ejecutar cuando el usuario intenta conectar

        # Etiqueta del título
        ttk.Label(self, text="Conectar a Servidor MySQL", font=("Helvetica", 16)).pack(pady=10)

        # Fila para ingresar el host, por defecto "localhost"
        self.host_entry = self._entry_row("Host:", "localhost")
        # Fila para ingresar el usuario, por defecto "root"
        self.user_entry = self._entry_row("Usuario:", "root")
        # Fila para ingresar la contraseña, oculta con "*"
        self.pass_entry = self._entry_row("Contraseña:", "", show="*")

        # Botón para intentar la conexión
        ttk.Button(self, text="Conectar", command=self._on_login).pack(pady=20)

        # Etiqueta para mostrar mensajes de error (inicialmente vacía)
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.pack()

    # Método auxiliar que crea una fila de entrada con etiqueta y campo de texto
    def _entry_row(self, label, default, show=None):
        frame = ttk.Frame(self)              # Contenedor horizontal para la fila
        frame.pack(fill="x", pady=5)         # Empaca el frame con espacio vertical
        ttk.Label(frame, text=label, width=15).pack(side="left")  # Etiqueta alineada a la izquierda
        entry = ttk.Entry(frame, show=show)  # Campo de entrada, opcionalmente con ocultación de texto
        entry.insert(0, default)             # Inserta el valor por defecto
        entry.pack(side="left", fill="x", expand=True)  # Ajuste y expansión del campo
        return entry                         # Devuelve el campo de entrada

    # Método que se ejecuta al presionar el botón "Conectar"
    def _on_login(self):
        # Recolecta los valores ingresados por el usuario
        data = {
            "host": self.host_entry.get(),
            "user": self.user_entry.get(),
            "password": self.pass_entry.get()
        }
        # Llama al callback con esos datos para manejar la conexión
        self.login_callback(data)

    # Método para mostrar mensajes de error en pantalla
    def show_error(self, message):
        self.error_label.config(text=message)

        #test
