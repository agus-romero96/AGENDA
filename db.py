import sqlite3
from datetime import datetime

# Crear la conexión a la base de datos
def conectar():
    return sqlite3.connect("agenda.db")

# Crear las tablas necesarias
def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)

    # Tabla de eventos con fecha
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        evento TEXT NOT NULL,
        dia TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    """)

    conexion.commit()
    conexion.close()

# Función para registrar un usuario
def registrar_usuario(usuario, contrasena):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Función para verificar el usuario
def verificar_usuario(usuario, contrasena):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    usuario_encontrado = cursor.fetchone()
    conexion.close()
    return usuario_encontrado is not None

# Función para agregar un evento
def agregar_evento(usuario, evento, dia, fecha, hora=None):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Obtener el ID del usuario
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
        usuario_id = cursor.fetchone()
        if usuario_id:
            cursor.execute("""
                INSERT INTO eventos (usuario_id, evento, dia, fecha, hora)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario_id[0], evento, dia, fecha, hora))
            conexion.commit()
        conexion.close()
    except Exception as e:
        print("Error al agregar el evento:", e)

# Función para obtener eventos de un usuario
def obtener_eventos(usuario):
    conexion = conectar()
    cursor = conexion.cursor()

    # Obtener el ID del usuario
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    usuario_id = cursor.fetchone()
    eventos = []
    if usuario_id:
        cursor.execute("""
            SELECT id, evento, dia, fecha, hora
            FROM eventos
            WHERE usuario_id = ?
        """, (usuario_id[0],))
        eventos = cursor.fetchall()

    conexion.close()
    return eventos

# Función para eliminar un evento
def eliminar_evento(evento_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conexion.commit()
    conexion.close()

# Función para modificar un evento
def modificar_evento(evento_id, nuevo_evento, nueva_fecha=None, nueva_hora=None):
    conexion = conectar()
    cursor = conexion.cursor()

    # Actualizar evento con fecha y hora si se proporcionan
    query = "UPDATE eventos SET evento = ?"
    parametros = [nuevo_evento]
    if nueva_fecha:
        query += ", fecha = ?"
        parametros.append(nueva_fecha)
    if nueva_hora:
        query += ", hora = ?"
        parametros.append(nueva_hora)

    query += " WHERE id = ?"
    parametros.append(evento_id)

    cursor.execute(query, tuple(parametros))
    conexion.commit()
    conexion.close()

# Función para obtener eventos por fecha
def obtener_eventos_por_fecha(usuario, fecha):
    conexion = conectar()
    cursor = conexion.cursor()

    # Obtener el ID del usuario
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    usuario_id = cursor.fetchone()
    eventos = []
    if usuario_id:
        cursor.execute("""
            SELECT id, evento, dia, hora
            FROM eventos
            WHERE usuario_id = ? AND fecha = ?
        """, (usuario_id[0], fecha))
        eventos = cursor.fetchall()

    conexion.close()
    return eventos

# Crear las tablas al inicializar el archivo
if __name__ == "__main__":
    crear_tablas()

    # Ejemplo de uso
    if registrar_usuario("usuario1", "password123"):
        print("Usuario registrado correctamente.")
    else:
        print("El usuario ya existe.")

    # Agregar un evento
    agregar_evento("usuario1", "Reunión de trabajo", "Lunes", "2024-06-12", "14:00")

    # Obtener eventos
    print("Eventos:")
    for evento in obtener_eventos("usuario1"):
        print(evento)

    # Modificar un evento
    modificar_evento(1, "Reunión actualizada", nueva_fecha="2024-06-13", nueva_hora="15:00")

    # Obtener eventos por fecha
    print("Eventos para 2024-06-13:")
    for evento in obtener_eventos_por_fecha("usuario1", "2024-06-13"):
        print(evento)

    # Eliminar un evento
    eliminar_evento(1)
    print("Evento eliminado.")
