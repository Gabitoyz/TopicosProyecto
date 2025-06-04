import tkinter as tk
import ttkbootstrap as ttk  # Usamos ttkbootstrap para estilos modernos
from modelo.base_de_datos import DatabaseConnection  # Clase para manejar conexión a la base de datos
from viista.login_view import LoginView         # Vista de login
from viista.base_de_datos_selector import DatabaseSelector  # Vista para seleccionar base de datos
from viista.main_view import MainView           # Vista principal con el gestor de consultas

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Cliente de Base de Datos (MySQL)")  # Título de la ventana
        self.geometry("600x500")                               # Tamaño inicial de la ventana
        self.style = ttk.Style("cosmo")                        # Tema para la visualizacion
        self.db = None                                         # Conexión activa (objeto DatabaseConnection)
        self.show_login()                                      # Inicia mostrando la vista del login

    def show_login(self):
        # Limpia la ventana y muestra el formulario de login
        for widget in self.winfo_children():
            widget.destroy()
        self.login_view = LoginView(self, self.load_databases)

    def load_databases(self, data):
        # Intenta conectarse al servidor MySQL con los datos ingresados
        self.temp_credentials = data  # Guarda las credenciales temporalmente
        db = DatabaseConnection(
            host=data["host"],
            database=None,
            user=data["user"],
            password=data["password"]
        )
        if db.connect_to_server():
            # Si se conecta al servidor, carga la lista de bases de datos
            databases = db.get_databases()
            self.show_database_selector(databases)
        else:
            # Si falla, muestra error en la vista de login
            self.login_view.show_error("No se pudo conectar al servidor. Verifica tus datos.")

    def show_database_selector(self, databases):
        # Limpia y muestra el selector de bases de datos
        for widget in self.winfo_children():
            widget.destroy()
        self.db_selector = DatabaseSelector(self, databases, self.try_login)

    def try_login(self, selected_database):
        # Intenta conectar a la base de datos seleccionada
        data = self.temp_credentials.copy()
        data["database"] = selected_database
        self.db = DatabaseConnection(**data)
        if self.db.connect():
            self.show_main()  # Conexión exitosa, procede pasar a la vista principal
        else:
            self.show_login()
            self.login_view.show_error("Error de conexión con la base de datos.")

    def show_main(self):
        # Muestra la vista principal (consulta y visualización de datos)
        for widget in self.winfo_children():
            widget.destroy()
        self.main_view = MainView(self, self.run_query)

        # Obtiene las tablas y columnas de la base y las muestra en el panel izquierdo
        tables = self.db.get_tables()
        tables_fields = {t: self.db.get_columns(t) for t in tables}
        self.main_view.show_tables(tables_fields)

    def run_query(self, query):
        # Ejecuta una consulta SQL y muestra resultados o errores
        try:
            cols, data = self.db.execute_query(query)
            self.main_view.show_results(cols, data)
        except Exception as e:
            self.main_view.show_results(["Error"], [[str(e)]])
