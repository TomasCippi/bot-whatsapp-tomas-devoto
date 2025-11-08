# functions/verificar_webhook.py
from flask import request
from colorama import Fore, Style
import os
from dotenv import load_dotenv

load_dotenv()

def verificar_webhook():
    """
    Verifica el webhook de WhatsApp Cloud API
    """
    token_verificacion = os.getenv("TOKEN_VERIFICACION")
    modo = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    desafio = request.args.get("hub.challenge")

    if modo == "subscribe" and token == token_verificacion:
        print(f"{Fore.GREEN}✓ Webhook verificado correctamente{Style.RESET_ALL}")
        return desafio, 200
    else:
        print(f"{Fore.RED}✗ Token de verificación inválido{Style.RESET_ALL}")
        return "Token inválido", 403
