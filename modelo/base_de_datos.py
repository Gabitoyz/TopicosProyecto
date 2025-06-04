# Importa el conector de MySQL y su clase de error
import mysql.connector
from mysql.connector import Error

# Clase para manejar la conexión a una base de datos MySQL
class DatabaseConnection:
    # Constructor de la clase: recibe los datos de conexión
    def __init__(self, host, database, user, password):
        self.host = host          # Dirección del servidor (localhost, IP, etc.)
        self.database = database  # Nombre de la base de datos
        self.user = user          # Usuario de MySQL
        self.password = password  # Contraseña del usuario
        self.conn = None          # Objeto de conexión, inicialmente nulo

    # Método para conectarse directamente a una base de datos específica
    def connect(self):
        try:
            # Intenta crear una conexión con todos los parámetros
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            # Devuelve True si la conexión fue exitosa
            return self.conn.is_connected()
        except Error:
            # Si ocurre un error, retorna False
            return False

    # Método alternativo para conectarse solo al servidor (sin seleccionar base de datos)
    def connect_to_server(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return self.conn.is_connected()
        except Error:
            return False

    # Método para obtener la lista de todas las bases de datos en el servidor
    def get_databases(self):
        cursor = self.conn.cursor()          # Crea un cursor para ejecutar la consulta
        cursor.execute("SHOW DATABASES")     # Ejecuta el comando SQL
        return [db[0] for db in cursor.fetchall()]  # Devuelve una lista de nombres de bases de datos

    # Método para obtener todas las tablas de la base de datos actual
    def get_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")        # Comando SQL para listar tablas
        return [t[0] for t in cursor.fetchall()]  # Lista de nombres de tablas

    # Método para obtener los nombres de columnas de una tabla dada
    def get_columns(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")  # Describe la estructura de la tabla
        return [col[0] for col in cursor.fetchall()]  # Lista los nombres de las columnas

    # Método para ejecutar una consulta SQL arbitraria (SELECT, INSERT, etc.)
    def execute_query(self, query):
        cursor = self.conn.cursor()       # Crea el cursor
        cursor.execute(query)             # Ejecuta la consulta

        if cursor.with_rows:              # Si la consulta devuelve filas (SELECT)
            data = cursor.fetchall()      # Recupera los datos
            headers = [desc[0] for desc in cursor.description]  # Recupera los encabezados
            return headers, data          # Devuelve tupla (encabezados, filas)
        else:
            self.conn.commit()            # Si no hay resultados (ej. INSERT), hace commit
            return None, []               # Retorna vacío
