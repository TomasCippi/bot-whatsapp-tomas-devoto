import os
import requests
from colorama import Fore, Style
from dotenv import load_dotenv
from mimetypes import guess_type

# --- Cargar configuración ---
load_dotenv()

VERSION = os.getenv("WHATSAPP_API_VERSION")
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TOKEN = os.getenv("META_TOKEN")

if not all([VERSION, PHONE_ID, TOKEN]):
    print(f"{Fore.RED}⚠️ Faltan variables en el archivo .env{Style.RESET_ALL}")
    exit()

# --- Constantes ---
URL = f"https://graph.facebook.com/{VERSION}/{PHONE_ID}/media"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 🔥 RUTA CORREGIDA 🔥
# Desde "functions/" subir a la carpeta raíz y luego entrar en "assets"
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "assets")


# --- Detectar tipo de archivo según extensión ---
def detectar_tipo_archivo(nombre_archivo: str):
    ext = nombre_archivo.lower()
    if ext.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return "image"
    elif ext.endswith((".mp3", ".ogg", ".m4a", ".wav")):
        return "audio"
    elif ext.endswith((".pdf", ".docx", ".txt")):
        return "document"
    elif ext.endswith((".webp", ".sticker")):
        return "sticker"
    else:
        return "desconocido"


# --- Subir un archivo individual ---
def subir_archivo(ruta_archivo: str, tipo: str):
    """Sube un archivo a la API de Meta y devuelve su ID."""
    try:
        with open(ruta_archivo, "rb") as f:
            mime_type, _ = guess_type(ruta_archivo)
            files = {"file": (os.path.basename(ruta_archivo), f, mime_type or "application/octet-stream")}
            data = {"messaging_product": "whatsapp"}
            response = requests.post(URL, headers=HEADERS, files=files, data=data)

        if response.status_code == 200:
            media_id = response.json().get("id")
            return media_id
        else:
            print(f"{Fore.RED}✗ Error al subir {os.path.basename(ruta_archivo)} ({response.status_code}): {response.text}{Style.RESET_ALL}")
            return None

    except Exception as e:
        print(f"{Fore.RED}✗ Error al subir archivo {ruta_archivo}: {e}{Style.RESET_ALL}")
        return None


# --- Subir todos los archivos de la carpeta assets ---
def subir_todos():
    print(f"{Fore.CYAN}Subiendo archivos desde {ASSETS_FOLDER}{Style.RESET_ALL}")

    if not os.path.exists(ASSETS_FOLDER):
        print(f"{Fore.RED}⚠️ La carpeta 'assets' no existe.{Style.RESET_ALL}")
        return

    archivos = os.listdir(ASSETS_FOLDER)
    if not archivos:
        print(f"{Fore.YELLOW}⚠️ No hay archivos en 'assets'.{Style.RESET_ALL}")
        return

    for archivo in archivos:
        ruta = os.path.join(ASSETS_FOLDER, archivo)
        if os.path.isfile(ruta):
            tipo = detectar_tipo_archivo(archivo)
            if tipo == "desconocido":
                print(f"{Fore.YELLOW}⚠️ Tipo no soportado: {archivo}{Style.RESET_ALL}")
                continue

            media_id = subir_archivo(ruta, tipo)
            if media_id:
                print(f"{Fore.GREEN}✔ {archivo}{Style.RESET_ALL} [{tipo.upper()}] - id: {Fore.CYAN}{media_id}{Style.RESET_ALL}")

if __name__ == "__main__":
    subir_todos()
