import sqlite3
from datetime import datetime, timedelta
from functions.templates_messages import bienvenida_devuelta_mensaje
from colorama import Fore, Style
from functions.hash_utils import get_identifier_hash
DB_PATH = "database.db"

def normalizar_numero(numero: str) -> str:
    """Quita el 9 después del 54 en números celulares argentinos."""
    if numero.startswith("549"):
        return "54" + numero[3:]
    return numero

def add_user(nombre, numero_real):
    numero_hash = get_identifier_hash(numero_real)
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (nombre, numero, fecha_primera_vez)
        VALUES (?, ?, ?)
    """, (nombre, numero_hash, fecha_actual))
    conn.commit()
    conn.close()

def user_exists(numero_real):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE numero = ?", (numero_hash,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)

def get_user_state(numero_real):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT estado FROM users WHERE numero = ?", (numero_hash,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def set_user_state(numero_real, estado):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET estado = ? WHERE numero = ?", (estado, numero_hash))
    conn.commit()
    conn.close()

TIEMPO_BIENVENIDA = {"hours": 5, "minutes": 0, "seconds": 0}  # tiempo de espera para bienvenida devuelta

def verificar_bienvenida_devuelta(numero_real, nombre):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ultimo_mensaje_enviado FROM users WHERE numero = ?", (numero_hash,))
    row = cursor.fetchone()
    fecha_actual = datetime.now()

    # Si nunca se envió, enviar la bienvenida
    if not row or not row[0]:
        # No hacemos aquí return True, solo inicializamos la fecha sin enviar aún
        cursor.execute("""
            UPDATE users SET ultimo_mensaje_enviado = ? WHERE numero = ?
        """, (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
        conn.commit()
        conn.close()
        return False  # no se envía ahora, se hace después en el flujo principal

    ultimo_enviado = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
    diferencia = fecha_actual - ultimo_enviado

    conn.close()
    if diferencia >= timedelta(**TIEMPO_BIENVENIDA):
        bienvenida_devuelta_mensaje(numero_real, nombre)
        # Actualizar la fecha solo después de enviar
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET ultimo_mensaje_enviado = ? WHERE numero = ?
        """, (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
        conn.commit()
        conn.close()
        return True

    return False