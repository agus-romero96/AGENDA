import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar  # Calendario
from db import verificar_usuario, registrar_usuario, agregar_evento, obtener_eventos
import datetime

class AgendaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agenda Personal")
        self.root.geometry("500x500")
        self.root.configure(bg="#F0F8FF")  # Fondo claro

        self.mostrar_login()
        self.root.mainloop()

    # --- Ventana de Inicio de Sesión ---
    def mostrar_login(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Label(self.root, text="Usuario:", bg="#F0F8FF").pack()
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack()

        tk.Label(self.root, text="Contraseña:", bg="#F0F8FF").pack()
        self.contrasena_entry = tk.Entry(self.root, show="*")
        self.contrasena_entry.pack()

        tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#ADD8E6").pack(pady=10)
        tk.Button(self.root, text="Registrar Usuario", command=self.mostrar_registro, bg="#90EE90").pack()

    # --- Ventana de Registro ---
    def mostrar_registro(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Registrar Usuario", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Label(self.root, text="Nuevo Usuario:", bg="#F0F8FF").pack()
        self.nuevo_usuario_entry = tk.Entry(self.root)
        self.nuevo_usuario_entry.pack()

        tk.Label(self.root, text="Contraseña:", bg="#F0F8FF").pack()
        self.nueva_contrasena_entry = tk.Entry(self.root, show="*")
        self.nueva_contrasena_entry.pack()

        tk.Button(self.root, text="Registrar", command=self.registrar_usuario, bg="#90EE90").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_login, bg="#FFB6C1").pack()

    # --- Ventana Principal ---
    def mostrar_menu_eventos(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text=f"Bienvenido, {usuario}", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Button(self.root, text="Agregar Evento", command=lambda: self.mostrar_agregar_evento(usuario), bg="#ADD8E6").pack(pady=5)
        tk.Button(self.root, text="Ver Eventos", command=lambda: self.mostrar_eventos(usuario), bg="#ADD8E6").pack(pady=5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.mostrar_login, bg="#FFB6C1").pack(pady=10)

    # --- Ventana para Agregar Evento ---
    def mostrar_agregar_evento(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text="Agregar Evento", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        tk.Label(self.root, text="Evento:", bg="#F0F8FF").pack()
        self.evento_entry = tk.Entry(self.root)
        self.evento_entry.pack()

        # Calendario para seleccionar fecha
        tk.Label(self.root, text="Seleccionar Fecha:", bg="#F0F8FF").pack()
        self.calendario = Calendar(self.root, date_pattern="yyyy-mm-dd")
        self.calendario.pack(pady=10)

        tk.Button(self.root, text="Guardar", command=lambda: self.guardar_evento(usuario), bg="#90EE90").pack(pady=10)
        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_menu_eventos(usuario), bg="#FFB6C1").pack()

    # --- Ventana para Ver Eventos ---
    def mostrar_eventos(self, usuario):
        self.limpiar_ventana()

        tk.Label(self.root, text="Tus Eventos", font=("Arial", 18), bg="#F0F8FF").pack(pady=20)

        eventos = obtener_eventos(usuario)
        if not eventos:
            tk.Label(self.root, text="No hay eventos programados.", bg="#F0F8FF").pack()
        else:
            for evento, dia in eventos:
                tk.Label(self.root, text=f"{dia}: {evento}", bg="#F0F8FF").pack()

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_menu_eventos(usuario), bg="#FFB6C1").pack(pady=10)

        # Simular notificación
        self.notificar_eventos(eventos)

    # --- Funciones de Manejo ---
    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        if verificar_usuario(usuario, contrasena):
            self.mostrar_menu_eventos(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar_usuario(self):
        usuario = self.nuevo_usuario_entry.get()
        contrasena = self.nueva_contrasena_entry.get()
        if registrar_usuario(usuario, contrasena):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.mostrar_login()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")

    def guardar_evento(self, usuario):
        evento = self.evento_entry.get()
        fecha = self.calendario.get_date()
        if evento and fecha:
            agregar_evento(usuario, evento, fecha)
            messagebox.showinfo("Éxito", "Evento guardado correctamente.")
            self.mostrar_menu_eventos(usuario)
        else:
            messagebox.showerror("Error", "Completa todos los campos.")

    def notificar_eventos(self, eventos):
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        for evento, fecha in eventos:
            if fecha == hoy:
                messagebox.showinfo("Notificación", f"Tienes un evento hoy: {evento}")

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Ejecutar la aplicación
if __name__ == "__main__":
    AgendaApp()
