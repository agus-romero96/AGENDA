from db import conectar_db

def agregar_evento(usuario, evento, fecha, dia):
    """Agrega un nuevo evento a la base de datos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    usuario_id = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO eventos (usuario_id, evento, fecha, dia) VALUES (?, ?, ?, ?)", 
                   (usuario_id, evento, fecha, dia))
    conexion.commit()
    conexion.close()

def eliminar_evento(evento_id):
    """Elimina un evento de la base de datos por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conexion.commit()
    conexion.close()
class Usuario:
    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena

class Evento:
    def __init__(self, id, usuario_id, evento, dia, fecha, hora):
        self.id = id
        self.usuario_id = usuario_id
        self.evento = evento
        self.dia = dia
        self.fecha = fecha
        self.hora = hora

    def __str__(self):
        hora_evento = f" a las {self.hora}" if self.hora else ""
        return f"{self.fecha}{hora_evento} - {self.evento}"
