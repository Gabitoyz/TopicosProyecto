# Importa ttkbootstrap para widgets con estilos modernos
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import ttk as tkk  # Se usa para los Treeview y Scrollbars clásicos

# Vista principal de la aplicación
class MainView(ttk.Frame):
    def __init__(self, parent, query_callback):
        super().__init__(parent, padding=10)  # Inicializa el frame con padding
        self.pack(fill="both", expand=True)   # Expande el frame para ocupar toda el área
        self.query_callback = query_callback  # Callback que se usará para ejecutar la consulta SQL

        # Crea un panel dividido horizontalmente (izquierda: tablas, derecha: consultas/resultados)
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        paned.pack(fill="both", expand=True)

        # Panel izquierdo con las tablas y sus campos
        self.tables_frame = ttk.LabelFrame(paned, text="Tablas y campos", padding=10)
        self.tables_frame.pack_propagate(False)  # Evita que el frame se redimensione según contenido
        self.tables_list = tkk.Treeview(self.tables_frame)  # Árbol para mostrar tablas y columnas
        self.tables_list.heading("#0", text="Tablas")  # Título del árbol
        self.tables_list.pack(fill="both", expand=True)
        paned.add(self.tables_frame, width=250)  # Agrega el panel izquierdo al panel dividido

        # Panel derecho donde se escribe la consulta y se muestran resultados
        right_frame = ttk.Frame(paned, padding=10)
        paned.add(right_frame, stretch="always")

        # Cuadro de texto para escribir la consulta SQL
        self.query_text = tk.Text(right_frame, height=3, font=("Courier", 11))
        self.query_text.pack(fill="x", padx=5, pady=(0, 10))  # Margen inferior

        # Botón para ejecutar la consulta escrita
        ttk.Button(
            right_frame,
            text="Ejecutar Consulta",
            command=self._run_query,
            bootstyle="primary"
        ).pack(pady=(0, 10))

        # Frame donde se mostrarán los resultados de la consulta
        self.result_frame = ttk.Frame(right_frame)
        self.result_frame.pack(fill="both", expand=True)

        # Árbol para mostrar los resultados de la consulta con encabezados
        self.result_tree = tkk.Treeview(self.result_frame, show="headings")
        self.result_tree.pack(side="left", fill="both", expand=True)

        # Scrollbars vertical y horizontal para los resultados
        vsb = tkk.Scrollbar(self.result_frame, orient="vertical", command=self.result_tree.yview)
        hsb = tkk.Scrollbar(self.result_frame, orient="horizontal", command=self.result_tree.xview)
        self.result_tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

    # Método privado que obtiene el texto de consulta y llama al callback
    def _run_query(self):
        query = self.query_text.get("1.0", "end").strip()  # Lee desde la línea 1, carácter 0, hasta el final
        if query:
            self.query_callback(query)  # Ejecuta la consulta usando el callback

    # Muestra los resultados en el árbol de resultados
    def show_results(self, headers, rows):
        self.result_tree.delete(*self.result_tree.get_children())  # Borra resultados anteriores
        self.result_tree["columns"] = headers  # Define las columnas
        for col in headers:
            self.result_tree.heading(col, text=col, anchor="center")  # Encabezado centrado
            self.result_tree.column(col, width=120, anchor="center")  # Tamaño y alineación de columna
        for row in rows:
            self.result_tree.insert("", "end", values=row)  # Inserta fila por fila

    # Muestra las tablas y sus columnas en el árbol izquierdo
    def show_tables(self, table_dict):
        self.tables_list.delete(*self.tables_list.get_children())  # Limpia el árbol
        for table, columns in table_dict.items():
            table_id = self.tables_list.insert("", "end", text=table, open=False)  # Inserta tabla
            for col in columns:
                self.tables_list.insert(table_id, "end", text=col)  # Inserta columnas dentro de la tabla
