import sqlite3
from datetime import datetime, timedelta
from colorama import Fore, Style
from functions.hash_utils import get_identifier_hash
from functions.send_messages import send_text_message
DB_PATH = "database.db"

def normalizar_numero(numero: str) -> str:
    """Quita el 9 después del 54 en números celulares argentinos."""
    if numero.startswith("549"):
        return "54" + numero[3:]
    return numero

def add_user(nombre, numero_real):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO users (nombre, numero, fecha_primera_vez, conversacion_iniciada, estado, ultimo_mensaje)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, numero_hash, fecha_actual, 1, 1, fecha_actual))
    conn.commit()
    conn.close()
    print(f"{Fore.GREEN}Nuevo usuario agregado: {nombre} | hash: {numero_hash[:12]}... | fecha: {fecha_actual}{Style.RESET_ALL}")
    send_text_message(numero_real, f"¡Hola {nombre}! Bienvenido/a al Tomás Devoto 😄")

def user_exists(numero_real):
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE numero = ?", (numero_hash,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)
