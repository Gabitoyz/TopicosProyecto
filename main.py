# Importa la clase App desde el módulo 'app' que está en la carpeta 'controlador'
# Esta clase representa la aplicación principal que contiene la lógica y la interfaz
from controlador.app import App

# Punto de entrada principal del programa
if __name__ == "__main__":
    # Crea una instancia de la aplicación
    app = App()

    # Inicia el bucle principal de la interfaz gráfica de usuario
    # Este método mantiene la ventana activa y escucha eventos (como clics o escritura)
    app.mainloop()
