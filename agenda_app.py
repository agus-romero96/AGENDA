import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar  # Calendario
from db import verificar_usuario, registrar_usuario, agregar_evento, obtener_eventos
import datetime

class AgendaApp:
    def __init__(self):  # Corregido el nombre del constructor
        self.root = tk.Tk()
        self.root.title("Agenda Personal")
        self.root.geometry("900x700")
        self.root.configure(bg="#EAF8F8")  # Fondo claro y moderno

        self.style = ttk.Style()
        self.style.theme_use("default")  # Asegurar compatibilidad
        self.style.configure("TButton", font=("Helvetica", 11), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 12))

        self.mostrar_login()
        self.root.mainloop()

    # --- Ventana de Inicio de Sesión ---
    def mostrar_login(self):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#EAF8F8", padx=20, pady=20)
        frame.pack(expand=True)

        # Encabezado
        tk.Label(frame, text="¡Bienvenido!", font=("Helvetica", 22, "bold"), bg="#EAF8F8", fg="#1C7C7D").pack(pady=10)
        tk.Label(frame, text="Inicia sesión para acceder a tu agenda", font=("Helvetica", 14), bg="#EAF8F8").pack(pady=5)

        # Campo de usuario
        tk.Label(frame, text="Usuario", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=5, anchor="w")
        self.usuario_entry = ttk.Entry(frame, width=30)
        self.usuario_entry.pack(pady=5)

        # Campo de contraseña
        tk.Label(frame, text="Contraseña", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=5, anchor="w")
        self.contrasena_entry = ttk.Entry(frame, show="*", width=30)
        self.contrasena_entry.pack(pady=5)

        # Botones
        ttk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion, style="TButton").pack(pady=10)
        ttk.Button(frame, text="Registrarse", command=self.mostrar_registro).pack()

    # --- Ventana de Registro ---
    def mostrar_registro(self):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#EAF8F8", padx=20, pady=20)
        frame.pack(expand=True)

        # Encabezado
        tk.Label(frame, text="¡Hola!", font=("Helvetica", 22, "bold"), bg="#EAF8F8", fg="#1C7C7D").pack(pady=10)
        tk.Label(frame, text="Regístrate para crear tu cuenta", font=("Helvetica", 14), bg="#EAF8F8").pack(pady=5)

        # Campos de registro
        tk.Label(frame, text="Nuevo Usuario", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=5, anchor="w")
        self.nuevo_usuario_entry = ttk.Entry(frame, width=30)
        self.nuevo_usuario_entry.pack(pady=5)

        tk.Label(frame, text="Contraseña", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=5, anchor="w")
        self.nueva_contrasena_entry = ttk.Entry(frame, show="*", width=30)
        self.nueva_contrasena_entry.pack(pady=5)

        # Botones
        ttk.Button(frame, text="Registrar", command=self.registrar_usuario).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.mostrar_login).pack()

    # --- Ventana Principal ---
    def mostrar_menu_eventos(self, usuario):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#EAF8F8", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado
        tk.Label(frame, text=f"Hola, {usuario}", font=("Helvetica", 22, "bold"), bg="#EAF8F8", fg="#1C7C7D").pack(pady=10)
        tk.Label(frame, text="¿Qué deseas hacer hoy?", font=("Helvetica", 14), bg="#EAF8F8").pack(pady=5)

        # Botones principales
        ttk.Button(frame, text="Agregar Evento", command=lambda: self.mostrar_agregar_evento(usuario)).pack(pady=10)
        ttk.Button(frame, text="Ver Eventos", command=lambda: self.mostrar_eventos(usuario)).pack(pady=10)
        ttk.Button(frame, text="Cerrar Sesión", command=self.mostrar_login).pack(pady=20)

    # --- Ventana para Agregar Evento ---
    def mostrar_agregar_evento(self, usuario):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#EAF8F8", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado
        tk.Label(frame, text="Agregar Evento", font=("Helvetica", 22, "bold"), bg="#EAF8F8", fg="#1C7C7D").pack(pady=10)

        # Campo para el nombre del evento
        tk.Label(frame, text="Nombre del Evento", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=5, anchor="w")
        self.evento_entry = ttk.Entry(frame, width=30)
        self.evento_entry.pack(pady=5)

        # Calendario
        tk.Label(frame, text="Seleccionar Fecha", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=10)
        self.calendario = Calendar(frame, date_pattern="yyyy-mm-dd")
        self.calendario.pack(pady=10)

        # Botones
        ttk.Button(frame, text="Guardar", command=lambda: self.guardar_evento(usuario)).pack(pady=10)
        ttk.Button(frame, text="Volver", command=lambda: self.mostrar_menu_eventos(usuario)).pack()

    # --- Ventana para Ver Eventos ---
    def mostrar_eventos(self, usuario):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#EAF8F8", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado
        tk.Label(frame, text="Tus Eventos", font=("Helvetica", 22, "bold"), bg="#EAF8F8", fg="#1C7C7D").pack(pady=10)

        # Mostrar eventos
        eventos = obtener_eventos(usuario)
        if not eventos:
            tk.Label(frame, text="No hay eventos programados.", font=("Helvetica", 12), bg="#EAF8F8").pack(pady=10)
        else:
            for evento, fecha in eventos:
                tk.Label(frame, text=f"{fecha}: {evento}", font=("Helvetica", 12), bg="#EAF8F8").pack(anchor="w", pady=2)

        ttk.Button(frame, text="Volver", command=lambda: self.mostrar_menu_eventos(usuario)).pack(pady=20)

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
if __name__ == "__main__":  # Corrección del identificador
    AgendaApp()
