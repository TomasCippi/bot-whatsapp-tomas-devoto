import sqlite3
import os
from flask import Flask, request
from colorama import Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functions.verify_webhook import verify_webhook
from functions.db_utils import *
from functions.hash_utils import *
from functions.send_messages import *
from functions.templates_messages import *

DB_PATH = "database.db"

# ------------------- Limpiar tabla users para pruebas -------------------
""" conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM users")
conn.commit()
conn.close()
print(Fore.YELLOW + "🧹 Tabla users limpiada para pruebas" + Style.RESET_ALL)  """

load_dotenv()
app = Flask(__name__)

TIEMPO_BIENVENIDA = {"hours": 5, "minutes": 0, "seconds": 0}  # tiempo de espera para bienvenida devuelta

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

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    return verify_webhook()

@app.route("/webhook", methods=["POST"])
def webhook_receive():
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

        print(f"{Fore.CYAN}📩 Mensaje recibido de {nombre} ({numero_real}): '{texto_usuario}'{Style.RESET_ALL}")

        # Verificar usuario
        if not user_exists(numero_real):
            print(f"Usuario nuevo: {numero_real}")
            add_user(nombre, numero_real)
            bienvenida_mensaje(numero_real, nombre)
            set_user_state(numero_real, 0)  # estado inicial
            return "EVENT_RECEIVED", 200

        if not update_conversation(numero_real):
            return "EVENT_RECEIVED", 200

        if verificar_bienvenida_devuelta(numero_real, nombre):
            return "EVENT_RECEIVED", 200
        # --- Manejo de estado ---
        estado_actual = get_user_state(numero_real)
        # --------------------------- Menu principal --------------------------- #
        if estado_actual == 0:
            # Menú principal
            if texto_usuario == "main_menu_opt1":  # Sobre Nosotros
                sobre_nosotros_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt2":  # Nivel Inicial
                set_user_state(numero_real, 2.1)
                nivel_inicial_message(numero_real)
            elif texto_usuario == "main_menu_opt3":  # Nivel Primario
                set_user_state(numero_real, 2.2)
                nivel_primario_message(numero_real)
            elif texto_usuario == "main_menu_opt4":  # Nivel Secundario
                set_user_state(numero_real, 2.3)
                nivel_secundario_message(numero_real)
            elif texto_usuario == "main_menu_opt5": # Contacto
                contacto_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt6": # Inscripciones
                pass
            else:
                main_error(numero_real)
        # --------------------------- Mensajes sobre nivel inicial 📘 --------------------------- #
        elif estado_actual == 2.1:
            # Nivel Inicial
            if texto_usuario == "menu_nivel_inicial_opt1":
                nivel_inicial_propuestas_pedagogicas(numero_real)

            elif texto_usuario == "menu_nivel_inicial_opt2":
                nivel_inicial_talleres_optativos(numero_real)

            elif texto_usuario == "menu_nivel_inicial_opt3":
                nivel_inicial_servicios_adicionales(numero_real)

            elif texto_usuario == "menu_nivel_inicial_opt4":
                nivel_inicial_horarios(numero_real)

            elif texto_usuario == "menu_nivel_inicial_opt5":
                set_user_state(numero_real, 0)
                main_menu_devuelta(numero_real)

            else:
                nivel_inicial_error(numero_real)
        # --------------------------- Mensajes sobre nivel primario 📙 --------------------------- #
        elif estado_actual == 2.2:
            # Nivel Inicial
            if texto_usuario == "menu_nivel_primario_opt1":
                nivel_primario_propuestas_pedagogicas(numero_real)

            elif texto_usuario == "menu_nivel_primario_opt2":
                nivel_primario_talleres_optativos(numero_real)

            elif texto_usuario == "menu_nivel_primario_opt3":
                nivel_primario_algunos_proyectos(numero_real)

            elif texto_usuario == "menu_nivel_primario_opt4":
                nivel_primario_servicios_adicionales(numero_real)

            elif texto_usuario == "menu_nivel_primario_opt5":
                nivel_primario_horarios(numero_real)

            elif texto_usuario == "menu_nivel_primario_opt6":
                set_user_state(numero_real, 0)
                main_menu_devuelta(numero_real)

            else:
                nivel_primario_error(numero_real)

        # --------------------------- Mensajes sobre nivel secundario 📕 --------------------------- #
        elif estado_actual == 2.3:
            # Nivel Secundario
            if texto_usuario == "menu_nivel_secundario_opt1":
                nivel_secundario_propuestas_pedagogicas(numero_real)
            elif texto_usuario == "menu_nivel_secundario_opt2":
                nivel_secundario_algunos_proyectos(numero_real)
            elif texto_usuario == "menu_nivel_secundario_opt3":
                nivel_secundario_planes_estudio(numero_real)
            
            elif texto_usuario == "menu_nivel_secundario_opt4":
                nivel_secundario_horarios(numero_real)
            
            elif texto_usuario == "menu_nivel_secundario_opt5":
                set_user_state(numero_real, 0)
                main_menu_devuelta(numero_real)

            else:
                nivel_secundario_error(numero_real)

    except Exception as e:
        print(Fore.RED + "Error procesando mensaje en main:" + Style.RESET_ALL, e)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(Fore.CYAN + f"🚀 Servidor corriendo en http://0.0.0.0:{port}" + Style.RESET_ALL)
    app.run(host="0.0.0.0", port=port, debug=True)
