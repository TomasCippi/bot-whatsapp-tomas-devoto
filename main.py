from flask import Flask, request, jsonify
from colorama import Fore, Style
from dotenv import load_dotenv
import os
import logging
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor

from functions.verificar_webhook import verificar_webhook
from functions.consola_logs import *
from functions.mensajes_funciones import mensaje_lista, mensaje_texto, mensaje_imagen
from functions.db_funciones import (
    verificar_numero,
    insertar_usuario,
    limpiar_usuarios,
    agregar_a_blacklist,
    remover_de_blacklist,
    numero_en_blacklist,
    cambiar_estado_usuario,
    obtener_estado_usuario,
    hash_numero,
    get_connection
)
from functions.templates import *

load_dotenv()

app = Flask(__name__)

# ------------------------------
# BD CONEXIÓN GLOBAL
# ------------------------------
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# ------------------------------
# CONTROL DE LOGS
# ------------------------------
def imprimir_logs():
    if os.getenv("IMPRIMIR_LOGS_FLASK") == "True":
        print("🟢 Logs de Flask activos")
    else:
        logging.getLogger('werkzeug').disabled = True
        app.logger.disabled = True
        print("🛑 Logs de Flask desactivados")

# ------------------------------
# WEBHOOK VERIFICACIÓN
# ------------------------------
@app.route("/webhook", methods=["GET"])
def verificar():
    return verificar_webhook()

# ------------------------------
# WEBHOOK MENSAJES
# ------------------------------
@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    try:
        data = request.json
        entry = data.get("entry", [])[0]
        cambio = entry.get("changes", [])[0].get("value", {})

        if "messages" not in cambio:
            return "EVENT_RECEIVED", 200

        mensaje = cambio["messages"][0]
        tipo = mensaje.get("type")

        # ------------------------------
        # DATOS DEL CONTACTO
        # ------------------------------
        contacto = cambio["contacts"][0]
        nombre = contacto["profile"].get("name", "Desconocido")

        # --- Número forzado para pruebas ---
        numero_real = "541158633864"
        numero_hash = hash_numero(numero_real)

        timestamp = mensaje.get("timestamp", "0")

        # ------------------------------
        # TEXTO DEL MENSAJE
        # ------------------------------
        if tipo == "text":
            texto = mensaje["text"]["body"]

        elif tipo == "interactive":
            interactivo = mensaje["interactive"]
            if "list_reply" in interactivo:
                titulo = interactivo["list_reply"]["title"]
                menu_id = interactivo["list_reply"]["id"]
                texto = f"{titulo} [MENU {menu_id}]"
            elif "button_reply" in interactivo:
                titulo = interactivo["button_reply"]["title"]
                menu_id = interactivo["button_reply"]["id"]
                texto = f"{titulo} [BOTÓN {menu_id}]"
            else:
                texto = "[INTERACTIVO DESCONOCIDO]"
        else:
            texto = f"[{tipo.upper()}]"

        # ------------------------------
        # BLACKLIST
        # ------------------------------
        if numero_en_blacklist(numero_hash):
            return "EVENT_RECEIVED", 200

        # Mostrar mensaje
        mensaje_log_recibido(nombre, numero_real, texto, timestamp)

        # ------------------------------
        # CHECK DE USUARIO
        # ------------------------------
        if not verificar_numero(numero_hash):
            if insertar_usuario(numero_hash, nombre):
                mensaje_log_usuario_agregado(numero_real, nombre)
                cambiar_estado_usuario(conn, numero_hash, 0)
                template_bienvenida(numero_real, nombre)
            else:
                mensaje_log_error(f"No se pudo insertar {numero_real}")
                return "EVENT_RECEIVED", 200
        else:
            template_bienvenida_devuelta(numero_real, nombre)

        # ------------------------------
        # ESTADO DEL USUARIO
        # ------------------------------
        estado = obtener_estado_usuario(conn, numero_hash)
        if estado is None:
            cambiar_estado_usuario(conn, numero_hash, 0)
            estado = 0

        # ------------------------------
        # MÁQUINA DE ESTADOS
        # ------------------------------
        if estado == 0:
            # Enviamos menú principal si es estado 0
            template_menu_principal(numero_real, "En qué podemos ayudarte hoy?")

            if tipo == "interactive":
                menu_id = None
                if "list_reply" in mensaje.get("interactive", {}):
                    menu_id = mensaje["interactive"]["list_reply"]["id"]
                elif "button_reply" in mensaje.get("interactive", {}):
                    menu_id = mensaje["interactive"]["button_reply"]["id"]

                if menu_id == "menu_principal_opt1":
                    cambiar_estado_usuario(conn, numero_hash, 1)
                    template_sobre_nosotros(numero_real)

                elif menu_id == "menu_principal_opt2":
                    cambiar_estado_usuario(conn, numero_hash, 2)
                    template_nivel_inicial(numero_real)

                elif menu_id == "menu_principal_opt3":
                    cambiar_estado_usuario(conn, numero_hash, 3)
                    template_nivel_primario(numero_real)

                elif menu_id == "menu_principal_opt4":
                    cambiar_estado_usuario(conn, numero_hash, 4)
                    template_nivel_secundario(numero_real)

                elif menu_id == "menu_principal_opt5":
                    cambiar_estado_usuario(conn, numero_hash, 5)
                    template_contacto(numero_real)

                elif menu_id == "menu_principal_opt6":
                    cambiar_estado_usuario(conn, numero_hash, 6)
                    template_inscripciones(numero_real)

        # ------------------------------
        # OTROS ESTADOS
        # ------------------------------

    except Exception as e:
        mensaje_log_error(f"Error procesando mensaje: {e}")

    return "EVENT_RECEIVED", 200

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    limpiar_usuarios()  # Solo para pruebas
    imprimir_logs()
    app.run(debug=True, port=5000)
