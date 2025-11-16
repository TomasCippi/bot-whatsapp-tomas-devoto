from flask import Flask, request, jsonify
from colorama import Fore, Style
from dotenv import load_dotenv
import os
import logging

from functions.verificar_webhook import verificar_webhook
from functions.consola_logs import *
from functions.mensajes_funciones import mensaje_lista, mensaje_texto, mensaje_imagen
from functions.db_funciones import verificar_numero, insertar_usuario, limpiar_usuarios, agregar_a_blacklist, remover_de_blacklist, numero_en_blacklist


load_dotenv()

app = Flask(__name__)

# --- Control de logs ---
def imprimir_logs():
    opcion = os.getenv("IMPRIMIR_LOGS_FLASK")
    if opcion == "True":
        print("🟢 Logs de Flask activos")
    else:
        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.logger.disabled = True
        print("🛑 Logs de Flask desactivados")

# --- Webhook de verificación (GET) ---
@app.route("/webhook", methods=["GET"])
def verificar():
    return verificar_webhook()

# --- Webhook de mensajes (POST) ---
@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    """Procesa los mensajes recibidos desde WhatsApp."""
    try:
        data = request.json
        entry = data.get("entry", [])[0]
        cambio = entry.get("changes", [])[0].get("value", {})

        # Si no hay mensajes, se ignora
        if "messages" not in cambio:
            return "EVENT_RECEIVED", 200

        mensaje = cambio["messages"][0]
        tipo = mensaje.get("type")

        # Datos del contacto
        contacto = cambio["contacts"][0]
        nombre = contacto["profile"].get("name", "Desconocido")
        numero = "541158633864"  # contacto.get("wa_id", "Sin número")
        timestamp = mensaje.get("timestamp", "0")

        # --- Procesamiento del mensaje según su tipo ---
        if tipo == "text":
            texto = mensaje["text"]["body"]

        elif tipo == "interactive":
            interactivo = mensaje.get("interactive", {})
            if "list_reply" in interactivo:
                texto = interactivo["list_reply"]["title"] + " [MENU INTERACTIVO]"
            elif "button_reply" in interactivo:
                texto = interactivo["button_reply"]["title"] + " [MENU INTERACTIVO]"
            else:
                texto = "<interacción desconocida> [MENU INTERACTIVO]"

        elif tipo == "audio":
            texto = "[AUDIO]"

        elif tipo == "document":
            texto = "[DOCUMENTO]"

        elif tipo == "sticker":
            texto = "[STICKER]"

        elif tipo == "image":
            texto = "[IMAGEN]"

        else:
            texto = f"<{tipo}>"

        # --- BLACKLIST ---
        if numero_en_blacklist(numero):
            # Si está en la blacklist: no mostrar logs, no procesar, no responder
            return "EVENT_RECEIVED", 200

        # --- Mostrar el mensaje recibido ---
        mensaje_log_recibido(nombre, numero, texto, timestamp)


        # --- CHECK DE USUARIO ---
        if not verificar_numero(numero):
            mensaje_log_alerta(f"El número [{numero}] no existe en la base de datos")
            if insertar_usuario(numero, nombre):
                mensaje_log_usuario_agregado(numero, nombre)
            else:
                mensaje_log_error(f"No se pudo agregar el usuario [{numero}]")
                return "EVENT_RECEIVED", 200  # Cortamos, no seguimos si falla


        # --- RESPUESTA DEL BOT ---
        if tipo in ["text", "interactive"]:
            mensaje_imagen("541158633864", 1368745011625382)

    except Exception as e:
        print("⚠️ Error procesando mensaje:", e)

    return "EVENT_RECEIVED", 200


# --- Ejecución principal ---
if __name__ == "__main__":
    # --- Limpieza automática para pruebas ---
    limpiar_tabla = True
    remover_de_blacklist("541158633864")

    if limpiar_tabla:
        limpiar_usuarios()
    else:
        pass

    imprimir_logs()
    app.run(debug=True, port=5000)
