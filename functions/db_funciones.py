import psycopg2
from psycopg2.extras import RealDictCursor
import os
import hashlib
from dotenv import load_dotenv
from functions.consola_logs import *

load_dotenv()

# --- Función para hashear números ---
def hash_numero(numero):
    secret = os.getenv("HASH_SECRET")
    if not secret:
        mensaje_log_error("HASH_SECRET no está definido en el archivo .env")
        return None

    combo = f"{numero}{secret}".encode("utf-8")
    return hashlib.sha256(combo).hexdigest()

# --- Conexión ---
def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        mensaje_log_error(f"Error al conectar a la base de datos: {e}")
        return None

# --- Verificar si el número existe (con hash) ---
def verificar_numero(numero):
    numero_hashed = hash_numero(numero)
    if not numero_hashed:
        return False

    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la base de datos.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE numero = %s LIMIT 1;", (numero_hashed,))
            existe = cur.fetchone()
            return existe is not None

    except Exception as e:
        mensaje_log_error(f"Error al verificar número: {e}")
        return False

    finally:
        conn.close()

# --- Verificar si un número está en la blacklist ---
def numero_en_blacklist(numero):
    numero_hashed = hash_numero(numero)
    if not numero_hashed:
        return False

    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la BD para verificar blacklist.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM blacklist WHERE numero_hash = %s LIMIT 1;",
                (numero_hashed,)
            )
            existe = cur.fetchone()
            return existe is not None

    except Exception as e:
        mensaje_log_error(f"Error al verificar blacklist: {e}")
        return False

    finally:
        conn.close()

# --- Insertar un nuevo usuario (numeros hashed) ---
def insertar_usuario(numero, nombre):
    numero_hashed = hash_numero(numero)
    if not numero_hashed:
        return False

    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la base de datos para insertar.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (numero, nombre) VALUES (%s, %s);",
                (numero_hashed, nombre)
            )
            conn.commit()
            return True

    except Exception as e:
        mensaje_log_error(f"Error al insertar usuario: {e}")
        return False

    finally:
        conn.close()

# --- Añadir un número a la blacklist ---
def agregar_a_blacklist(numero):
    numero_hashed = hash_numero(numero)
    if not numero_hashed:
        return False

    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la BD para agregar a la blacklist.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO blacklist (numero_hash) VALUES (%s) ON CONFLICT DO NOTHING;",
                (numero_hashed,)
            )
            conn.commit()

            mensaje_log_alerta(f"El numero [{numero}] fue agregado a blacklist.")

            return True

    except Exception as e:
        mensaje_log_error(f"Error al agregar el numero [{numero}] a la blacklist: {e}")
        return False

    finally:
        conn.close()


# --- Remover un número de la blacklist ---
def remover_de_blacklist(numero):
    numero_hashed = hash_numero(numero)
    if not numero_hashed:
        return False

    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la BD para remover de la blacklist.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM blacklist WHERE numero_hash = %s;",
                (numero_hashed,)
            )
            conn.commit()

            mensaje_log_alerta(f"El numero [{numero}] fue eliminado de la blacklist.")

            return True

    except Exception as e:
        mensaje_log_error(f"Error al remover el numero [{numero}] de la blacklist: {e}")
        return False

    finally:
        conn.close()

# --- Limpiar tabla (SOLO PARA PRUEBAS) ---
def limpiar_usuarios():
    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la base de datos para limpiar la tabla.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users;")
            conn.commit()
            mensaje_log_alerta("Tabla 'users' limpiada correctamente PARA PRUEBAS")
            return True

    except Exception as e:
        mensaje_log_error(f"Error al limpiar tabla users: {e}")
        return False

    finally:
        conn.close()
