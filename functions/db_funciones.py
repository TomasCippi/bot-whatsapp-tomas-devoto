import os
import hashlib
from datetime import datetime, timedelta
from functions.consola_logs import *
from functions.db_config import get_db_connection

# --- HASH ---
def hash_numero(numero: str) -> str | None:
    secret = os.getenv("HASH_SECRET")
    if not secret:
        return None
    return hashlib.sha256(f"{numero}{secret}".encode("utf-8")).hexdigest()

# --- USUARIOS ---
def verificar_numero(numero_hash: str) -> bool:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE numero = %s LIMIT 1;", (numero_hash,))
                return cur.fetchone() is not None
    except Exception as e:
        mensaje_log_error(f"Error verificar_numero: {e}")
        return False

def insertar_usuario(numero_hash: str, nombre: str) -> bool:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (numero, nombre, estado, ultimo_mensaje_enviado) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                    (numero_hash, nombre, 0, datetime.now())
                )
                conn.commit()
            return True
    except Exception as e:
        mensaje_log_error(f"Error insertar_usuario: {e}")
        return False

def limpiar_usuarios():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users;")
                conn.commit()
        mensaje_log_alerta("🧹 Tabla users limpiada")
        return True
    except Exception as e:
        mensaje_log_error(f"Error limpiar_usuarios: {e}")
        return False

# --- BLACKLIST ---
def numero_en_blacklist(numero_hash: str) -> bool:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM blacklist WHERE numero_hash = %s LIMIT 1;", (numero_hash,))
                return cur.fetchone() is not None
    except Exception as e:
        mensaje_log_error(f"Error blacklist: {e}")
        return False

# --- ESTADOS ---
def obtener_estado_usuario(numero_hash: str) -> int:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT estado FROM users WHERE numero = %s;", (numero_hash,))
                res = cur.fetchone()
                return res["estado"] if res else 0
    except Exception as e:
        mensaje_log_error(f"Error obtener_estado: {e}")
        return 0

def cambiar_estado_usuario(numero_hash: str, nuevo_estado: int) -> bool:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET estado = %s WHERE numero = %s;", (nuevo_estado, numero_hash))
                conn.commit()
        return True
    except Exception as e:
        mensaje_log_error(f"Error cambiar_estado: {e}")
        return False

# --- CONTROL TIEMPO ---
def control_ultimo_mensaje(numero_hash) -> bool:
    """
    Verifica si pasó el tiempo límite.
    Retorna True si se reseteó el estado (timeout).
    Retorna False si todo sigue igual.
    """
    # CONFIGURACION TIEMPO
    RESET_DIAS = 0
    RESET_HORAS = 10
    RESET_MINUTOS = 0
    RESET_SEGUNDOS = 0 

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ultimo_mensaje_enviado FROM users WHERE numero = %s;", (numero_hash,))
                res = cur.fetchone()
                
                if not res or not res.get("ultimo_mensaje_enviado"): 
                    return False

                ultimo = res["ultimo_mensaje_enviado"]

                if isinstance(ultimo, str):
                    try:
                        ultimo = datetime.fromisoformat(ultimo)
                    except ValueError:
                        return False

                tiempo_maximo = timedelta(
                    days=RESET_DIAS, 
                    hours=RESET_HORAS, 
                    minutes=RESET_MINUTOS, 
                    seconds=RESET_SEGUNDOS
                )
                
                tiempo_transcurrido = datetime.now() - ultimo

                if tiempo_transcurrido >= tiempo_maximo:
                    cambiar_estado_usuario(numero_hash, 0)
                    mensaje_log_alerta(f"⏳ Inactividad detectada ({tiempo_transcurrido}). Estado reseteado a 0.")
                    return True # AVISAMOS QUE HUBO RESET

    except Exception as e:
        mensaje_log_error(f"Error control_tiempo: {e}")
    
    return False

def registrar_envio(numero_hash: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET ultimo_mensaje_enviado = %s WHERE numero = %s;", (datetime.now(), numero_hash))
                conn.commit()
    except Exception as e:
        mensaje_log_error(f"Error registrar_envio: {e}")