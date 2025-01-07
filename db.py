import sqlite3
from datetime import datetime

def crear_tablas():
    conn = None
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        
        # Eliminar tablas si existen
        c.execute('DROP TABLE IF EXISTS materias')
        
        # Crear tabla de usuarios si no existe
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                     (usuario TEXT PRIMARY KEY, contrasena TEXT)''')
        
        # Crear tabla de materias con la estructura correcta
        c.execute('''CREATE TABLE IF NOT EXISTS materias
                     (usuario TEXT,
                      hora_dia TEXT,
                      materia TEXT,
                      PRIMARY KEY (usuario, hora_dia))''')
        
        # Crear tabla de deberes si no existe
        c.execute('''CREATE TABLE IF NOT EXISTS deberes
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      usuario TEXT,
                      materia TEXT,
                      descripcion TEXT,
                      fecha_entrega DATE)''')
        
        conn.commit()
        print("Tablas creadas correctamente")
        
    except Exception as e:
        print(f"Error al crear tablas: {str(e)}")
    finally:
        if conn:
            conn.close()

def obtener_deberes(usuario):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    
    c.execute('''SELECT materia, descripcion, fecha_entrega 
                 FROM deberes 
                 WHERE usuario = ? 
                 ORDER BY fecha_entrega''', (usuario,))
    
    deberes = c.fetchall()
    conn.close()
    return deberes

def guardar_deber(usuario, materia, descripcion, fecha):
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        
        c.execute('''INSERT INTO deberes (usuario, materia, descripcion, fecha_entrega)
                     VALUES (?, ?, ?, ?)''', (usuario, materia, descripcion, fecha))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al guardar deber: {e}")
        return False

def guardar_materias(usuario, horario):
    conn = None
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        
        # Verificar si la tabla existe
        c.execute('''CREATE TABLE IF NOT EXISTS materias
                     (usuario TEXT, 
                      hora_dia TEXT, 
                      materia TEXT,
                      PRIMARY KEY (usuario, hora_dia))''')
        
        print(f"=== DEBUG GUARDADO DE MATERIAS ===")
        print(f"Usuario: {usuario}")
        print(f"Horario a guardar: {horario}")
        
        # Primero eliminamos el horario existente del usuario
        c.execute('DELETE FROM materias WHERE usuario = ?', (usuario,))
        print(f"Registros eliminados para el usuario")
        
        # Insertamos el nuevo horario
        for hora_dia, materia in horario.items():
            print(f"Intentando insertar: {hora_dia} -> {materia}")
            c.execute('''INSERT INTO materias (usuario, hora_dia, materia)
                        VALUES (?, ?, ?)''', (usuario, hora_dia, materia))
        
        conn.commit()
        print("Commit realizado exitosamente")
        return True
        
    except sqlite3.Error as e:
        print(f"Error SQLite: {e}")
        return False
    except Exception as e:
        print(f"Error general: {type(e).__name__}")
        print(f"Descripción: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada")

def obtener_materias(usuario):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    
    print(f"\n=== DEBUG OBTENER MATERIAS ===")
    print(f"Buscando materias para usuario: {usuario}")
    
    c.execute('SELECT hora_dia, materia FROM materias WHERE usuario = ?', (usuario,))
    materias = dict(c.fetchall())
    
    print(f"Materias encontradas: {materias}")
    
    conn.close()
    return materias

# Las funciones existentes permanecen igual
def verificar_usuario(usuario, contrasena):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?',
              (usuario, contrasena))
    resultado = c.fetchone()
    conn.close()
    return resultado is not None

def registrar_usuario(usuario, contrasena):
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        c.execute('INSERT INTO usuarios VALUES (?, ?)', (usuario, contrasena))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def agregar_evento(usuario, evento, fecha):
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        
        # Crear tabla de eventos si no existe
        c.execute('''CREATE TABLE IF NOT EXISTS eventos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      usuario TEXT,
                      evento TEXT,
                      fecha DATE)''')
        
        c.execute('INSERT INTO eventos (usuario, evento, fecha) VALUES (?, ?, ?)',
                 (usuario, evento, fecha))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al agregar evento: {e}")
        return False

def obtener_eventos(usuario):
    try:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        
        c.execute('SELECT evento, fecha FROM eventos WHERE usuario = ? ORDER BY fecha',
                 (usuario,))
        eventos = c.fetchall()
        
        conn.close()
        return eventos
    except Exception as e:
        print(f"Error al obtener eventos: {e}")
        return []

# Asegúrate de crear las tablas cuando se importa el módulo
crear_tablas()