from flask import request
from colorama import Fore, Style
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del .env

def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    expected_token = os.getenv("VERIFY_TOKEN")

    print(Fore.CYAN + "📥 Webhook recibido:" + Style.RESET_ALL)
    print(f"{Fore.YELLOW}🔐 Token recibido: {token}{Style.RESET_ALL}")

    if mode == "subscribe" and token == expected_token:
        print(Fore.GREEN + "✅ Verificación exitosa, enviando challenge! 🚀" + Style.RESET_ALL)
        return challenge, 200
    else:
        print(Fore.RED + "❌ Verificación fallida: Token inválido." + Style.RESET_ALL)
        return "Invalid verification", 403
