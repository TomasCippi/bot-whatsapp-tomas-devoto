import os
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from functions.consola_logs import mensaje_log_error, mensaje_log_alerta

load_dotenv()

# Crear el pool de conexiones UNA sola vez al iniciar
try:
    pool = ThreadedConnectionPool(
        minconn=1,
        maxconn=20,
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )
    mensaje_log_alerta("🟢 Pool de conexiones a BD iniciado.")
except Exception as e:
    mensaje_log_error(f"Error fatal iniciando Pool de BD: {e}")
    pool = None

@contextmanager
def get_db_connection():
    """
    Entrega una conexión del pool y la devuelve al terminar.
    Uso: with get_db_connection() as conn: ...
    """
    if pool is None:
        raise Exception("El pool de conexiones no está inicializado.")
    
    conn = pool.getconn()
    try:
        yield conn
    finally:
        # Importante: No cerramos la conexión, la devolvemos al pool
        pool.putconn(conn)