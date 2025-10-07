import hmac
import hashlib
import sqlite3
import os
import sys
from flask import Flask, request
from colorama import Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functions.verify_webhook import verify_webhook
from functions.db_utils import normalizar_numero, add_user, user_exists, get_user_state, set_user_state, verificar_bienvenida_devuelta
from functions.hash_utils import get_identifier_hash
from functions.templates_messages import *

DB_PATH = "database.db"

APP_SECRET = os.getenv("APP_SECRET")  # tu secreto de Meta

# ------------------- Validar firma -------------------
def verify_signature():
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        print(Fore.RED + "❌ Request sin firma" + Style.RESET_ALL)
        return False

    body = request.get_data()  # cuerpo raw del POST
    expected_signature = "sha256=" + hmac.new(
        APP_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    # Comparación segura
    if not hmac.compare_digest(expected_signature, signature):
        print(Fore.RED + "❌ Firma inválida" + Style.RESET_ALL)
        return False

    return True
# ------------------- Validar firma -------------------


# ------------------- Limpiar tabla users para pruebas -------------------
def limpiar_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print(Fore.YELLOW + "🧹 Tabla users limpiada para pruebas" + Style.RESET_ALL)

# ------------------- Limpiar tabla users para pruebas -------------------


load_dotenv()
app = Flask(__name__)

clean_log = True  # True = silencia los logs de Flask, False = los muestra

if clean_log:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # solo errores graves aparecerán


# --------------------- LOGS --------------------- #
LOG_DIR = "logs"

original_stdout = sys.stdout

class DailyLogger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        # Crear carpeta si no existe
        os.makedirs(self.log_dir, exist_ok=True)

        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.log_file = open(os.path.join(self.log_dir, f"{self.current_date}.log"), "a", encoding="utf-8", buffering=1)

    def write(self, message):
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            # Fecha cambió → cerrar archivo viejo y abrir uno nuevo
            self.log_file.close()
            self.current_date = today
            self.log_file = open(os.path.join(self.log_dir, f"{self.current_date}.log"), "a", encoding="utf-8", buffering=1)

        self.log_file.write(message)
        self.log_file.flush()
        original_stdout.write(message)
        original_stdout.flush()

    def flush(self):
        self.log_file.flush()
        original_stdout.flush()

# Redirigir stdout
sys.stdout = DailyLogger(LOG_DIR)
# --------------------- LOGS --------------------- #

def update_conversation(numero_real):
    """Actualiza fecha y cuenta de conversación si pasaron menos de 24h."""
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ultimo_mensaje FROM users WHERE numero = ?", (numero_hash,))
    row = cursor.fetchone()
    fecha_actual = datetime.now()

    if row and row[0]:
        ultimo_msg = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        diferencia = fecha_actual - ultimo_msg
        if diferencia < timedelta(hours=24):
            cursor.execute("""
                UPDATE users 
                SET conversacion_iniciada = conversacion_iniciada + 1,
                    ultimo_mensaje = ?
                WHERE numero = ?
            """, (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
            conn.commit()
            conn.close()
            return True
        else:
            cursor.execute("UPDATE users SET ultimo_mensaje = ? WHERE numero = ?",
                        (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
            conn.commit()
            conn.close()
            return False
    conn.close()
    return True

def manejo_menu(estado_actual, numero_hash, nombre, numero_real, texto_usuario):
    if estado_actual == 0:
        # Menú principal
        if texto_usuario == "main_menu_opt1":  # Sobre Nosotros
            sobre_nosotros_mensaje(numero_hash, nombre, numero_real)
        elif texto_usuario == "main_menu_opt2":  # Nivel Inicial
            set_user_state(numero_real, 2.1)
            nivel_inicial_message(numero_hash, nombre, numero_real)
        elif texto_usuario == "main_menu_opt3":  # Nivel Primario
            set_user_state(numero_real, 2.2)
            nivel_primario_message(numero_hash, nombre, numero_real)
        elif texto_usuario == "main_menu_opt4":  # Nivel Secundario
            set_user_state(numero_real, 2.3)
            nivel_secundario_message(numero_hash, nombre, numero_real)
        elif texto_usuario == "main_menu_opt5":  # Contacto
            contacto_mensaje(numero_hash, nombre, numero_real)
        elif texto_usuario == "main_menu_opt6":  # Inscripciones
            pass
        else:
            main_error(numero_hash, nombre, numero_real)

    # --------------------------- Mensajes sobre nivel inicial 📘 --------------------------- #
    elif estado_actual == 2.1:
        if texto_usuario == "menu_nivel_inicial_opt1":
            nivel_inicial_propuestas_pedagogicas(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_inicial_opt2":
            nivel_inicial_talleres_optativos(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_inicial_opt3":
            nivel_inicial_servicios_adicionales(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_inicial_opt4":
            nivel_inicial_horarios(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_inicial_opt5":
            set_user_state(numero_real, 0)
            main_menu_devuelta(numero_hash, nombre, numero_real)
        else:
            nivel_inicial_error(numero_hash, nombre, numero_real)

    # --------------------------- Mensajes sobre nivel primario 📙 --------------------------- #
    elif estado_actual == 2.2:
        if texto_usuario == "menu_nivel_primario_opt1":
            nivel_primario_propuestas_pedagogicas(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_primario_opt2":
            nivel_primario_talleres_optativos(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_primario_opt3":
            nivel_primario_algunos_proyectos(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_primario_opt4":
            nivel_primario_servicios_adicionales(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_primario_opt5":
            nivel_primario_horarios(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_primario_opt6":
            set_user_state(numero_real, 0)
            main_menu_devuelta(numero_hash, nombre, numero_real)
        else:
            nivel_primario_error(numero_hash, nombre, numero_real)

    # --------------------------- Mensajes sobre nivel secundario 📕 --------------------------- #
    elif estado_actual == 2.3:
        if texto_usuario == "menu_nivel_secundario_opt1":
            nivel_secundario_propuestas_pedagogicas(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_secundario_opt2":
            nivel_secundario_algunos_proyectos(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_secundario_opt3":
            nivel_secundario_planes_estudio(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_secundario_opt4":
            nivel_secundario_horarios(numero_hash, nombre, numero_real)
        elif texto_usuario == "menu_nivel_secundario_opt5":
            set_user_state(numero_real, 0)
            main_menu_devuelta(numero_hash, nombre, numero_real)
        else:
            nivel_secundario_error(numero_hash, nombre, numero_real)

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    return verify_webhook()

@app.route("/webhook", methods=["POST"])
def webhook_receive():
    # -------------------- VALIDAR FIRMA -------------------- #
    if not verify_signature():
        return "Forbidden", 403

    data = request.json
    try:
        entry = data['entry'][0]
        change = entry['changes'][0]['value']

        # Ignorar si no hay mensajes
        if 'messages' not in change or not change['messages']:
            return "EVENT_RECEIVED", 200

        contacto = change['contacts'][0]
        nombre = contacto['profile']['name']
        numero_real = normalizar_numero(contacto['wa_id'])
        mensaje = change['messages'][0]

        # Determinar tipo de mensaje
        texto_usuario = None
        if 'text' in mensaje and 'body' in mensaje['text'] and mensaje['text']['body'].strip():
            texto_usuario = mensaje['text']['body'].strip().lower()
        elif 'interactive' in mensaje and mensaje['interactive']['type'] == 'list_reply' and 'id' in mensaje['interactive']['list_reply']:
            texto_usuario = mensaje['interactive']['list_reply']['id']

        # Si no hay texto → ignorar
        if not texto_usuario:
            return "EVENT_RECEIVED", 200

        # Después de determinar texto_usuario
        mensaje_id = mensaje['id']

        # Evitar procesar mensajes duplicados (último ID recibido)
        numero_hash = get_identifier_hash(numero_real)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT ultimo_id_recibido FROM users WHERE numero = ?", (numero_hash,))
        row = cursor.fetchone()
        if row and row[0] == mensaje_id:
            # Mensaje idéntico al último recibido → ignorar
            conn.close()
            return "EVENT_RECEIVED", 200

        # Guardar como último mensaje recibido
        cursor.execute("""
            UPDATE users SET ultimo_id_recibido = ? WHERE numero = ?
        """, (mensaje_id, numero_hash))
        conn.commit()
        conn.close()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hash_corto = numero_hash[:8]  # solo los primeros 8 caracteres del hash

        print(f"{Fore.YELLOW}[{timestamp}] 📩 Mensaje recibido de {nombre} | hash={hash_corto} | '{texto_usuario}'{Style.RESET_ALL}")

        # Verificar usuario
        if not user_exists(numero_real):
            print(f"{Fore.BLUE}[{timestamp}] 👤 Usuario nuevo agregado: {nombre} | hash={hash_corto} {Style.RESET_ALL}")
            add_user(nombre, numero_real)
            bienvenida_mensaje(numero_hash, nombre, numero_real)
            set_user_state(numero_real, 0)  # estado inicial
            return "EVENT_RECEIVED", 200

        if not update_conversation(numero_real):
            return "EVENT_RECEIVED", 200

        if verificar_bienvenida_devuelta(numero_real, nombre):
            return "EVENT_RECEIVED", 200
        # --- Manejo de estado ---
        estado_actual = get_user_state(numero_real)
        # --------------------------- Menu principal --------------------------- #
        
        print(numero_real)

        manejo_menu(estado_actual, numero_hash, nombre, numero_real, texto_usuario)

    except Exception as e:
        print(Fore.RED + "Error procesando mensaje en main:" + Style.RESET_ALL, e)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    limpiar_table()
    port = int(os.getenv("PORT", 5000))
    print(Fore.CYAN + f"🚀 Servidor corriendo en http://0.0.0.0:{port}" + Style.RESET_ALL)
    app.run(host="0.0.0.0", port=port, debug=True)
