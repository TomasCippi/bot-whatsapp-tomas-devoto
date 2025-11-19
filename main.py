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

import re

def normalizar_numero(numero: str) -> str:
    """
    Limpia y normaliza un número de WhatsApp (solo para Argentina 54 11).
    
    1. Elimina todos los caracteres no numéricos.
    2. Elimina el '+'.
    3. Para 54 11, elimina el '9' que puede venir después del código de país.
    4. Maneja el prefijo '15' si aparece.
    """
    
    # 1. Elimina todos los caracteres no numéricos, excepto el '+' inicial
    numero_limpio = re.sub(r'[^0-9+]', '', numero)
    
    # 2. Elimina el '+' si existe
    if numero_limpio.startswith('+'):
        numero_limpio = numero_limpio[1:]
        
    # 3. Normalización específica para Argentina (54)
    if numero_limpio.startswith('54'):
        # Caso: 54 9 11... -> Eliminar el '9'
        # El 9 debe estar en la posición 3 (índice 2)
        if len(numero_limpio) > 3 and numero_limpio[2] == '9' and numero_limpio[3:5] == '11':
            # Ejemplo: 54911xxxxxxx -> 5411xxxxxxx
            return numero_limpio[:2] + numero_limpio[3:]
        
        # Caso: 54 11 15... -> Eliminar el '15'
        # El 15 (o 1115) se usa en algunos sistemas y debe ser 11
        if numero_limpio.startswith('541115'):
            # Ejemplo: 54111545678901 -> 541145678901
            # Nota: Esto es peligroso si el número real tiene 15 dígitos.
            # Una normalización más segura es limitarse a remover solo el '9'.
            pass # Para fines de la API de Meta, centrémonos en el '9'.

    # Si no es un caso conocido o no requiere limpieza de 9, devuelve el número
    return numero_limpio

# Ejemplos:
# print(normalizar_numero("54 9 11 4567-8901"))  # Debería dar '541145678901'
# print(normalizar_numero("541145678901"))      # Debería dar '541145678901'
# print(normalizar_numero("+5491145678901"))    # Debería dar '541145678901'

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
        #NUMERO_TEST = "541158633864"
        #numero_real = NUMERO_TEST 
        
        numero_normalizado = normalizar_numero(numero_origen)

        numero_real = numero_normalizado

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