import os
import glob
import requests
from dotenv import load_dotenv
from colorama import Fore, Style
import mimetypes

load_dotenv()

API_VERSION = os.getenv("META_API_VERSION")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
TOKEN = os.getenv("META_TOKEN")

valid_extensions = {
    # Audio
    ".aac", ".mp3", ".mp4a", ".mpeg", ".amr", ".ogg", ".opus", ".wav",
    # Video
    ".mp4", ".3gp", ".mov", ".avi", ".mkv",
    # Documentos Office
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    # Documentos PDF y texto
    ".pdf", ".txt", ".rtf",
    # Imágenes
    ".jpeg", ".jpg", ".png", ".webp", ".gif", ".bmp", ".tiff"
}

def upload_media_file(file_path: str):
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f, mime_type)
        }
        data = {
            "messaging_product": "whatsapp",
            "type": mime_type
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            media_id = response.json().get("id")
            print(Fore.GREEN + f"  ✓ {os.path.basename(file_path)} → media_id: {media_id}" + Style.RESET_ALL)
            return media_id
        else:
            print(Fore.RED + f"  ✕ Error subiendo {file_path}: {response.status_code}, {response.text}" + Style.RESET_ALL)
            return None

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
    print(Fore.CYAN + f"Subiendo archivos de la carpeta {base_dir}..." + Style.RESET_ALL)

    for file_path in glob.glob(os.path.join(base_dir, "*.*")):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in valid_extensions:
            upload_media_file(file_path)
        else:
            print(Fore.YELLOW + f"❌ Archivo no permitido para subir: {file_path}" + Style.RESET_ALL)
