import os
import requests
from colorama import Fore, Style
from dotenv import load_dotenv
from functions.consola_logs import mensaje_enviado, mensaje_recibido

# --- Configuración general ---
load_dotenv()

VERSION = os.getenv("WHATSAPP_API_VERSION")
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TOKEN = os.getenv("META_TOKEN")

if not all([VERSION, PHONE_ID, TOKEN]):
    print(f"{Fore.RED}⚠️ Faltan variables en el archivo .env{Style.RESET_ALL}")

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
            mensaje_enviado(numero, mensaje)
        else:
            print(f"{Fore.RED}✗ Error al enviar mensaje ({response.status_code}): {response.text}{Style.RESET_ALL}")
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}✗ Error al conectar con la API: {e}{Style.RESET_ALL}")
        return None

def mensaje_lista(numero: str, titulo: str, texto: str, footer: str, botones: list):
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
                    {
                        "rows": botones
                    }
                ]
            }
        }
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            mensaje_enviado(numero, "[Lista interactiva]")
        else:
            print(f"{Fore.RED}✗ Error al enviar lista ({response.status_code}): {response.text}{Style.RESET_ALL}")
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}✗ Error al conectar con la API: {e}{Style.RESET_ALL}")
        return None

def mensaje_imagen(numero: str, id_imagen: str, texto: str = None):
    """Envía una imagen por WhatsApp (con o sin texto)."""
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "image",
        "image": {
            "id": id_imagen
        }
    }

    # Si hay texto, lo agregamos al cuerpo
    if texto:
        payload["image"]["caption"] = texto

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            mensaje_enviado(numero, "[Imagen] " + texto if texto else "[Imagen sin texto]")
        else:
            print(f"{Fore.RED}✗ Error al enviar imagen ({response.status_code}): {response.text}{Style.RESET_ALL}")
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}✗ Error al conectar con la API: {e}{Style.RESET_ALL}")
        return None