import tkinter as tk

class MenuPrincipal(tk.Frame):
    def __init__(self, parent, callback_agregar, callback_ver_eventos, callback_cerrar):
        super().__init__(parent)
        self.callback_agregar = callback_agregar
        self.callback_ver_eventos = callback_ver_eventos
        self.callback_cerrar = callback_cerrar
        self.configurar_menu()

    def configurar_menu(self):
        tk.Label(self, text="Menú Principal", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(self, text="Agregar Evento", command=self.callback_agregar).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self, text="Ver Eventos", command=self.callback_ver_eventos).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self, text="Cerrar Sesión", command=self.callback_cerrar).grid(row=3, column=0, padx=10, pady=10)
