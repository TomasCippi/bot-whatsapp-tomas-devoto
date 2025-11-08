from flask import Flask, request, jsonify
from functions.verificar_webhook import verificar_webhook
from functions.consola_logs import mensaje_recibido
from functions.mensajes_funciones import mensaje_lista, mensaje_texto, mensaje_imagen
import logging

app = Flask(__name__)

# --- Control de logs ---
def imprimir_logs(opcion: bool):
    """Activa o desactiva los logs de Flask."""
    if opcion:
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
        numero = "541158633864" #contacto.get("wa_id", "Sin número")
        timestamp = mensaje.get("timestamp", "0")

        # --- Procesamiento del mensaje según su tipo ---
        if tipo == "text":
            texto = mensaje["text"]["body"]

        elif tipo == "interactive":
            # Puede ser una respuesta de lista o de botón
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
            # Cualquier otro tipo (imagen, audio, etc.)
            texto = f"<{tipo}>"

        # Mostrar el mensaje recibido en consola
        mensaje_recibido(nombre, numero, texto, timestamp)

        # --- RESPUESTA DEL BOT ---
        if tipo in ["text", "interactive"]:
            # Si es texto o respuesta del menú, responder con un mensaje + lista
            mensaje_imagen("541158633864", 1368745011625382)

    except Exception as e:
        print("⚠️ Error procesando mensaje:", e)

    return "EVENT_RECEIVED", 200


# --- Ejecución principal ---
if __name__ == "__main__":
    imprimir_logs(False)
    app.run(debug=True, port=5000)
