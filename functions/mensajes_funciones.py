import os
import requests
from colorama import Fore, Style
from dotenv import load_dotenv
from functions.consola_logs import *

# --- Configuración general ---
load_dotenv()

VERSION = os.getenv("WHATSAPP_API_VERSION")
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TOKEN = os.getenv("META_TOKEN")

if not all([VERSION, PHONE_ID, TOKEN]):
    mensaje_log_error("Faltan variables en el archivo .env. Revisá WHATSAPP_API_VERSION, WHATSAPP_PHONE_NUMBER_ID y META_TOKEN.")
    raise SystemExit("Faltan variables de entorno: revisá .env")

URL = f"https://graph.facebook.com/{VERSION}/{PHONE_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# --- Funciones de mensajes ---
def mensaje_texto(numero: str, mensaje: str):
    """Envía un mensaje de texto por WhatsApp"""
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensaje}
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            mensaje_log_enviado(numero, mensaje)
        else:
            mensaje_log_error(f"Error al enviar mensaje a [{numero}]({response.status_code}) | Detalle: {response.text}")
        return response.json()
    except Exception as e:
        mensaje_log_error(f"Error al conectar con la API: {e}")
        return None


def mensaje_lista(numero: str, titulo: str, texto: str, footer: str, botones: list, menu_id: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": texto},
            "footer": {"text": footer},
            "action": {
                "button": titulo,
                "sections": [
                    {"rows": botones}
                ]
            }
        }
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            mensaje_log_enviado(numero, f"[Lista interactiva '{menu_id}'] ")
        else:
            mensaje_log_error(f"Error al enviar lista a [{numero}]({response.status_code}) | Detalle: {response.text}")
        return response.json()
    except Exception as e:
        mensaje_log_error(f"Error al conectar con la API: {e}")
        return None


def mensaje_imagen(numero: str, id_imagen: str, texto: str = None):
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "image",
        "image": {"id": id_imagen}
    }

    if texto:
        payload["image"]["caption"] = texto

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            mensaje_log_enviado(numero, "[Imagen] " + texto if texto else "[Imagen sin texto]")
        else:
            mensaje_log_error(f"Error al enviar imagen a [{numero}]({response.status_code}) | Detalle: {response.text}")
        return response.json()
    except Exception as e:
        mensaje_log_error(f"Error al conectar con la API: {e}")
        return None