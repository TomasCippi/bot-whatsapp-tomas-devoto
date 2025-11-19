import os
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from functions.consola_logs import *

load_dotenv()


# =====================================================================
# 🔐 HASH DEL NÚMERO
# =====================================================================
def hash_numero(numero: str) -> str | None:
    secret = os.getenv("HASH_SECRET")
    if not secret:
        mensaje_log_error("HASH_SECRET no está definido en el archivo .env")
        return None
    return hashlib.sha256(f"{numero}{secret}".encode("utf-8")).hexdigest()


# =====================================================================
# 🔌 CONEXIÓN A LA BASE DE DATOS
# =====================================================================
def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        mensaje_log_error(f"Error al conectar a la base de datos: {e}")
        return None


# =====================================================================
# 👤 USUARIOS
# =====================================================================
def verificar_numero(numero_hash: str) -> bool:
    if not numero_hash:
        return False
    
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM users WHERE numero = %s LIMIT 1;",
                (numero_hash,)
            )
            return cur.fetchone() is not None

    except Exception as e:
        mensaje_log_error(f"Error al verificar número: {e}")
        return False

    finally:
        conn.close()


def insertar_usuario(numero_hash: str, nombre: str) -> bool:
    if not numero_hash:
        return False
    
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (numero, nombre, estado, ultimo_mensaje_enviado)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (numero_hash, nombre, 0, datetime.now())
            )
            conn.commit()
            return True

    except Exception as e:
        mensaje_log_error(f"Error al insertar usuario: {e}")
        return False

    finally:
        conn.close()


def limpiar_usuarios() -> bool:
    conn = get_connection()
    if not conn:
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


# =====================================================================
# 🛑 BLACKLIST
# =====================================================================
def numero_en_blacklist(numero_hash: str) -> bool:
    if not numero_hash:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM blacklist WHERE numero_hash = %s LIMIT 1;",
                (numero_hash,)
            )
            return cur.fetchone() is not None

    except Exception as e:
        mensaje_log_error(f"Error al verificar blacklist: {e}")
        return False

    finally:
        conn.close()


def agregar_a_blacklist(numero_hash: str) -> bool:
    if not numero_hash:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO blacklist (numero_hash) VALUES (%s) ON CONFLICT DO NOTHING;",
                (numero_hash,)
            )
            conn.commit()
            mensaje_log_alerta(f"El numero [{numero_hash}] fue agregado a blacklist.")
            return True

    except Exception as e:
        mensaje_log_error(f"Error al agregar a blacklist: {e}")
        return False

    finally:
        conn.close()


def remover_de_blacklist(numero_hash: str) -> bool:
    if not numero_hash:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM blacklist WHERE numero_hash = %s;", (numero_hash,))
            conn.commit()
            mensaje_log_alerta(f"El numero [{numero_hash}] fue eliminado de la blacklist.")
            return True

    except Exception as e:
        mensaje_log_error(f"Error al remover de blacklist: {e}")
        return False

    finally:
        conn.close()


# =====================================================================
# 🔄 ESTADOS
# =====================================================================
def obtener_estado_usuario(numero_hash: str) -> int | None:
    if not numero_hash:
        return None

    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT estado FROM users WHERE numero = %s;",
                (numero_hash,)
            )
            res = cur.fetchone()
            return res["estado"] if res else None

    except Exception as e:
        mensaje_log_error(f"Error al obtener estado del usuario {numero_hash}: {e}")
        return None

    finally:
        conn.close()


def cambiar_estado_usuario(numero_hash: str, nuevo_estado: int) -> bool:
    if not numero_hash:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET estado = %s WHERE numero = %s;",
                (nuevo_estado, numero_hash)
            )
            conn.commit()
            return True

    except Exception as e:
        mensaje_log_error(f"Error al cambiar estado del usuario {numero_hash}: {e}")
        return False

    finally:
        conn.close()


# =====================================================================
# 🕒 REGISTRAR ÚLTIMO MENSAJE ENVIADO
# =====================================================================
def registrar_envio(numero_hash: str):
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET ultimo_mensaje_enviado = %s
                WHERE numero = %s;
                """,
                (datetime.now(), numero_hash)
            )
            conn.commit()

    except Exception as e:
        mensaje_log_error(f"Error registrando envío: {e}")

    finally:
        conn.close()


# =====================================================================
# ⏳ CONTROL DE INACTIVIDAD (RESET DE ESTADO)
# =====================================================================
TIEMPO_RESET_HORAS = 5


def control_ultimo_mensaje(numero_hash):
    """
    Si pasaron más de X horas desde el último mensaje enviado por el BOT,
    resetea el estado del usuario.
    """

    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ultimo_mensaje_enviado
                FROM users
                WHERE numero = %s;
                """,
                (numero_hash,)
            )

            res = cur.fetchone()
            if not res:
                return

            ultimo = res.get("ultimo_mensaje_enviado")
            if not ultimo:
                return

            # Convertir fecha si viene como string
            if isinstance(ultimo, str):
                try:
                    ultimo = datetime.fromisoformat(ultimo)
                except:
                    try:
                        ultimo = datetime.strptime(ultimo, "%Y-%m-%d %H:%M:%S")
                    except:
                        mensaje_log_error(f"Formato inválido en ultimo_mensaje_enviado: {ultimo}")
                        return

            ahora = datetime.now()

            if ahora - ultimo >= timedelta(hours=TIEMPO_RESET_HORAS):
                cambiar_estado_usuario(numero_hash, 0)
                mensaje_log_info(f"⏳ Pasaron {TIEMPO_RESET_HORAS}h → estado reseteado a 0")

    except Exception as e:
        mensaje_log_error(f"Error en control_ultimo_mensaje(): {e}")

    finally:
        conn.close()
