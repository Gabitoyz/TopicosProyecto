# Importa la biblioteca ttkbootstrap para crear interfaces gráficas modernas basadas en ttk
import ttkbootstrap as ttk

# Define una clase que hereda de ttk.Frame para crear un componente visual de selección de base de datos
class DatabaseSelector(ttk.Frame):
    # Constructor de la clase: recibe el padre (ventana), la lista de bases de datos y un callback
    def __init__(self, parent, databases, select_callback):
        # Llama al constructor de la clase padre y aplica un relleno interno
        super().__init__(parent, padding=20)
        self.pack(fill="both", expand=True)  # Expande el frame para que ocupe todo el espacio
        self.select_callback = select_callback  # Guarda la función de callback que se llamará al seleccionar una base

        # Etiqueta instructiva
        ttk.Label(self, text="Selecciona una base de datos", font=("Helvetica", 14)).pack(pady=10)

        # ComboBox (menú desplegable) con la lista de bases de datos
        self.combo = ttk.Combobox(self, values=databases, state="readonly")
        self.combo.pack(pady=10)

        # Si hay al menos una base de datos, selecciona la primera por defecto
        if databases:
            self.combo.current(0)

        # Botón para confirmar selección y llamar al método _select()
        ttk.Button(self, text="Entrar", command=self._select).pack(pady=10)

    # Método privado que se ejecuta cuando se presiona el botón "Entrar"
    def _select(self):
        # Llama a la función de callback con el valor actualmente seleccionado del ComboBox
        self.select_callback(self.combo.get())
