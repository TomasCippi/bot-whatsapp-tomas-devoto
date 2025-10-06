import sqlite3
import os
from flask import Flask, request
from colorama import Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functions.verify_webhook import verify_webhook
from functions.db_utils import normalizar_numero, user_exists, add_user
from functions.hash_utils import get_identifier_hash
from functions.send_messages import send_text_message
from functions.templates_messages import *

DB_PATH = "database.db"

# ------------------- Limpiar tabla users para pruebas -------------------
""" conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM users")
conn.commit()
conn.close()
print(Fore.YELLOW + "🧹 Tabla users limpiada para pruebas" + Style.RESET_ALL) """

load_dotenv()
app = Flask(__name__)

TIEMPO_BIENVENIDA = {"hours": 5, "minutes": 0, "seconds": 0}  # tiempo de espera para bienvenida devuelta

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
    """
    Envía bienvenida devuelta si pasaron TIEMPO_BIENVENIDA desde el último mensaje enviado.
    Retorna True si se envió la bienvenida (ignorar el mensaje actual).
    """
    numero_hash = get_identifier_hash(numero_real)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ultimo_mensaje_enviado FROM users WHERE numero = ?", (numero_hash,))
    row = cursor.fetchone()
    fecha_actual = datetime.now()

    # Usuario nuevo o sin último mensaje enviado → enviar bienvenida
    if not row or not row[0]:
        bienvenida_devuelta_mensaje(numero_real, nombre)
        send_menu_list(numero_real, "¿En qué podemos ayudarte hoy?", opciones_menu_principal)
        cursor.execute("""
            UPDATE users SET ultimo_mensaje_enviado = ? WHERE numero = ?
        """, (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
        conn.commit()
        conn.close()
        return True

    ultimo_enviado = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
    diferencia = fecha_actual - ultimo_enviado

    if diferencia >= timedelta(**TIEMPO_BIENVENIDA):
        bienvenida_devuelta_mensaje(numero_real, nombre)
        cursor.execute("""
            UPDATE users SET ultimo_mensaje_enviado = ? WHERE numero = ?
        """, (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
        conn.commit()
        conn.close()
        return True

    conn.close()
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
        if user_exists(numero_real):
            if not update_conversation(numero_real):
                return "EVENT_RECEIVED", 200

            if verificar_bienvenida_devuelta(numero_real, nombre):
                return "EVENT_RECEIVED", 200

            # ---------------------- Respuestas de menú ----------------------
            if texto_usuario == "main_menu_opt1":
                sobre_nosotros_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt2":
                pass  # Nivel inicial
            elif texto_usuario == "main_menu_opt3":
                pass  # Nivel primario
            elif texto_usuario == "main_menu_opt4":
                pass  # Nivel secundario
            elif texto_usuario == "main_menu_opt5":
                contacto_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt6":
                pass  # Inscripciones
            elif texto_usuario == "..":
                mensaje_prueba(numero_real, nombre)
            else:
                send_text_message(numero_real, "No entendí el comando.")
        else:
            # Usuario nuevo
            add_user(nombre, numero_real)
            bienvenida_mensaje(numero_real, nombre)

    except Exception as e:
        print(Fore.RED + "Error procesando mensaje en main:" + Style.RESET_ALL, e)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(Fore.CYAN + f"🚀 Servidor corriendo en http://0.0.0.0:{port}" + Style.RESET_ALL)
    app.run(host="0.0.0.0", port=port, debug=True)
