from flask import request
from colorama import Fore, Style
from datetime import datetime

def listen_messages():
    data = request.json

    try:
        entry = data['entry'][0]
        change = entry['changes'][0]['value']

        if 'messages' not in change:
            return "EVENT_RECEIVED", 200

        nombre = change['contacts'][0]['profile']['name']
        numero = change['contacts'][0]['wa_id']
        mensaje = change['messages'][0]
        tipo = mensaje['type']

        texto = mensaje['text']['body'] if tipo == 'text' else '<no-text>'

        timestamp = int(mensaje['timestamp'])
        fecha_hora = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        print(
            f"{Fore.RED}name: {Fore.LIGHTYELLOW_EX}{nombre} {Style.RESET_ALL}| "
            f"{Fore.BLUE}number: {Fore.LIGHTYELLOW_EX}{numero} {Style.RESET_ALL}| "
            f"{Fore.GREEN}type: {Fore.LIGHTYELLOW_EX}{tipo} {Style.RESET_ALL}| "
            f"{Fore.MAGENTA}message: {Fore.LIGHTYELLOW_EX}{texto} "
            f"{Fore.CYAN}[{fecha_hora}]{Style.RESET_ALL}"
        )

    except Exception as e:
        print(Fore.RED + "Error processing message:" + Style.RESET_ALL, e)

    return "EVENT_RECEIVED", 200
