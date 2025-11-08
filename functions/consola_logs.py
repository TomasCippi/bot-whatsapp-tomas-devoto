from colorama import Fore, Style
from datetime import datetime

def mensaje_recibido(nombre, numero, texto, timestamp):
    try:
        fecha_hora = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

        # --- Log limpio y con color ---
        print(f"\n{Fore.LIGHTYELLOW_EX}──────── NUEVO MENSAJE RECIBIDO ────────{Style.RESET_ALL}")
        print(f"De: {Fore.YELLOW}{nombre}{Style.RESET_ALL} {Fore.BLUE}[{numero}] {Style.RESET_ALL}")
        print(f"Mensaje:{Fore.GREEN} '{texto}' {Style.RESET_ALL}")
        print(f"Fecha y hora:{Fore.MAGENTA} {fecha_hora} {Style.RESET_ALL}")
        print(f"{Fore.LIGHTYELLOW_EX}{'─'*40}{Style.RESET_ALL}")

    except Exception as e:
        print(Fore.RED + "Error procesando el mensaje:" + Style.RESET_ALL, e)

def mensaje_enviado(numero, texto):
    try:
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{Fore.CYAN}─────────── MENSAJE ENVIADO ───────────{Style.RESET_ALL}")
        print(f"A: {Fore.BLUE}[{numero}] {Style.RESET_ALL}")
        print(f"Mensaje:{Fore.GREEN} '{texto}' {Style.RESET_ALL}")
        print(f"Fecha y hora:{Fore.MAGENTA} {fecha_hora} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*40}{Style.RESET_ALL}")
    except Exception as e:
        print(Fore.RED + "Error mostrando mensaje enviado:" + Style.RESET_ALL, e)