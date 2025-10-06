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

# ------------------- Limpiar tabla users para pruebas -------------------
DB_PATH = "database.db"
""" conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DELETE FROM users")
conn.commit()
conn.close()
print(Fore.YELLOW + "🧹 Tabla users limpiada para pruebas" + Style.RESET_ALL) """

load_dotenv()
app = Flask(__name__)

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
            print(f"{Fore.YELLOW}Usuario ya registrado, conversación actualizada{Style.RESET_ALL}")
            return True  # Puede responder
        else:
            print(f"{Fore.MAGENTA}Pasaron más de 24h desde el último mensaje. No se responde.{Style.RESET_ALL}")
            cursor.execute("UPDATE users SET ultimo_mensaje = ? WHERE numero = ?",
                        (fecha_actual.strftime('%Y-%m-%d %H:%M:%S'), numero_hash))
            conn.commit()
            return False
    conn.close()
    return True

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    return verify_webhook()

@app.route("/webhook", methods=["POST"])
def webhook_receive():
    data = request.json
    try:
        entry = data['entry'][0]
        change = entry['changes'][0]['value']

        if 'messages' not in change or not change['messages']:
            return "EVENT_RECEIVED", 200  # ignorar mensajes vacíos

        # Extraer datos
        nombre = change['contacts'][0]['profile']['name']
        numero_real = normalizar_numero(change['contacts'][0]['wa_id'])
        mensaje = change['messages'][0]

        # Determinar tipo de mensaje
        if 'text' in mensaje and 'body' in mensaje['text'] and mensaje['text']['body'].strip():
            texto_usuario = mensaje['text']['body'].strip().lower()
        elif 'interactive' in mensaje and mensaje['interactive']['type'] == 'list_reply':
            texto_usuario = mensaje['interactive']['list_reply']['id']
        else:
            return "EVENT_RECEIVED", 200  # mensaje que no entendemos

        print(f"{Fore.CYAN}📩 Mensaje recibido de {nombre} ({numero_real}): '{texto_usuario}'{Style.RESET_ALL}")

        # Verificar existencia de usuario
        if user_exists(numero_real):
            puede_responder = update_conversation(numero_real)
            if not puede_responder:
                return "EVENT_RECEIVED", 200

            # ---------------------- Respuestas de menú ----------------------
            if texto_usuario == "main_menu_opt1":
                sobre_nosotros_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt2":
                pass  # Nivel inicial, aún sin plantilla
            elif texto_usuario == "main_menu_opt3":
                pass  # Nivel primario
            elif texto_usuario == "main_menu_opt4":
                pass  # Nivel secundario
            elif texto_usuario == "main_menu_opt5":
                contacto_mensaje(numero_real)
            elif texto_usuario == "main_menu_opt6":
                pass  # Inscripciones
            # Mensajes de prueba o comandos especiales
            elif texto_usuario == "..":
                mensaje_prueba(numero_real, nombre)
            # Mensajes no reconocidos
            else:
                send_text_message(numero_real, "No entendí el comando.")
        else:
            add_user(nombre, numero_real)
            bienvenida_mensaje(numero_real, nombre)

    except Exception as e:
        print(Fore.RED + "Error procesando mensaje en main:" + Style.RESET_ALL, e)

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(Fore.CYAN + f"🚀 Servidor corriendo en http://0.0.0.0:{port}" + Style.RESET_ALL)
    app.run(host="0.0.0.0", port=port, debug=True)
