# create_db.py
import sqlite3

# Nombre del archivo de base de datos (puede estar en la carpeta del proyecto)
DB_NAME = "database.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Crear tabla users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        numero TEXT NOT NULL UNIQUE,
        fecha_primera_vez TEXT NOT NULL,
        mensajes_enviados_usuario INTEGER DEFAULT 0,
        estado REAL DEFAULT 0,
        ultimo_mensaje_enviado TEXT,
        ultimo_id_recibido TEXT
    )
    """)

    # Crear tabla estadisticas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estadisticas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cantidad_usuarios INTEGER DEFAULT 0,
        conversaciones_iniciadas INTEGER DEFAULT 0,
        conversaciones_inscripcion INTEGER DEFAULT 0,
        mensajes_enviados INTEGER DEFAULT 0,
        mensajes_recibidos INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente en", DB_NAME)

if __name__ == "__main__":
    create_tables()
