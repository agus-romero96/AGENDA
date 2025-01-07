import sqlite3

def test_conexion():
    try:
        conn = sqlite3.connect('agenda.db')
        print("Conexión exitosa a la base de datos")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

test_conexion() 