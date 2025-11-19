from flask import Flask, request
from dotenv import load_dotenv
import threading
import logging

# --- IMPORTACIONES EXPLÍCITAS (SIN ASTERISCOS) ---
from functions.verificar_webhook import verificar_webhook
from functions.consola_logs import (
    mensaje_log_alerta, 
    mensaje_log_recibido, 
    mensaje_log_usuario_agregado, 
    mensaje_log_error
)
from functions.db_funciones import (
    hash_numero, 
    numero_en_blacklist, 
    verificar_numero, 
    insertar_usuario, 
    control_ultimo_mensaje, 
    obtener_estado_usuario, 
    registrar_envio, 
    limpiar_usuarios
)
from functions.templates import template_bienvenida, template_bienvenida_devuelta
from functions.maquina_estados import procesar_flujo

load_dotenv()
app = Flask(__name__)

# --- LOGS FLASK ---
log = logging.getLogger('werkzeug')
log.disabled = True 

# ==========================================
#  WORKER: Procesa el mensaje en segundo plano
# ==========================================
def worker_procesar_mensaje(data):
    """Esta función corre en un hilo separado para no trabar al bot"""
    try:
        cambio = data.get("entry", [])[0].get("changes", [])[0].get("value", {})
        if "messages" not in cambio: return

        mensaje = cambio["messages"][0]
        contacto = cambio["contacts"][0]
        
        # Datos del remitente original
        nombre = contacto["profile"].get("name", "Desconocido")
        numero_origen = mensaje.get("from")
        
        # 🔥 HARDCODEO SOLICITADO: Forzar envíos al número de prueba
        NUMERO_TEST = "541158633864"
        numero_real = NUMERO_TEST 
        
        # Hash del número
        numero_hash = hash_numero(numero_real)

        # Extracción de contenido
        tipo = mensaje.get("type")
        texto_log = ""
        interactive_id = None

        if tipo == "text":
            texto_log = mensaje["text"]["body"]
        elif tipo == "interactive":
            interactivo = mensaje["interactive"]
            if "list_reply" in interactivo:
                interactive_id = interactivo["list_reply"]["id"]
                texto_log = f"[MENU] {interactive_id}"
            elif "button_reply" in interactivo:
                interactive_id = interactivo["button_reply"]["id"]
                texto_log = f"[BOTON] {interactive_id}"
        else:
            texto_log = f"[{tipo.upper()}]"

        # --- 1. BLACKLIST CHECK ---
        if numero_en_blacklist(numero_hash):
            mensaje_log_alerta(f"Ignorando mensaje de blacklist: {numero_real}")
            return

        # --- 2. USUARIO NUEVO (Si entra aquí, se va y no chequea tiempo) ---
        if not verificar_numero(numero_hash):
            if insertar_usuario(numero_hash, nombre):
                mensaje_log_usuario_agregado(numero_real, nombre)
                template_bienvenida(numero_real, nombre)
                registrar_envio(numero_hash)
            return

        # --- 3. CHEQUEO DE TIEMPO (Solo usuarios existentes) ---
        # Si pasó el tiempo, control_ultimo_mensaje devuelve True
        if control_ultimo_mensaje(numero_hash):
            # Le damos la bienvenida de vuelta
            template_bienvenida_devuelta(numero_real, nombre)
            # Registramos este envío para resetear el contador de tiempo
            registrar_envio(numero_hash)
            # IMPORTANTE: Cortamos aquí. No procesamos lo que escribió el usuario,
            # porque priorizamos saludarlo y mostrarle el menú.
            return 

        # --- 4. FLUJO NORMAL (Si no es nuevo y no pasó el tiempo) ---
        estado_actual = obtener_estado_usuario(numero_hash)
        mensaje_log_recibido(nombre, numero_real, texto_log, estado_actual)
        
        procesar_flujo(numero_real, numero_hash, estado_actual, tipo, texto_log, interactive_id)
        
        registrar_envio(numero_hash)

    except Exception as e:
        mensaje_log_error(f"Error en worker: {e}")

# ==========================================
#  RUTAS FLASK
# ==========================================
@app.route("/webhook", methods=["GET"])
def verificar():
    return verificar_webhook()

@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.json
    thread = threading.Thread(target=worker_procesar_mensaje, args=(data,))
    thread.start()
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    limpiar_usuarios()
    mensaje_log_alerta("🚀 BOT INICIADO - Modo Prueba (Número Hardcodeado)")
    app.run(debug=True, port=5000)