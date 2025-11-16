import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from functions.consola_logs import *

load_dotenv()

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


# --- Verificar si el número existe ---
def verificar_numero(numero):
    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la base de datos.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE numero = %s LIMIT 1;", (numero,))
            existe = cur.fetchone()
            return existe is not None

    except Exception as e:
        mensaje_log_error(f"Error al verificar número: {e}")
        return False

    finally:
        conn.close()


# --- Insertar un nuevo usuario ---
def insertar_usuario(numero, nombre):
    conn = get_connection()
    if not conn:
        mensaje_log_alerta("No se pudo conectar a la base de datos para insertar.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (numero, nombre) VALUES (%s, %s);",
                (numero, nombre)
            )
            conn.commit()

            # log del usuario nuevo agregado
            mensaje_log_usuario_agregado(numero, nombre)

            return True

    except Exception as e:
        mensaje_log_error(f"Error al insertar usuario: {e}")
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
            mensaje_log_alerta("Tabla 'users' limpiada correctamente.")
            return True

    except Exception as e:
        mensaje_log_error(f"Error al limpiar tabla users: {e}")
        return False

    finally:
        conn.close()
