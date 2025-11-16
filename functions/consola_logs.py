from colorama import Fore, Style
from datetime import datetime

# --- Helper general ---
def _ahora():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# --- Mensaje recibido ---
def mensaje_log_recibido(nombre, numero, texto, timestamp):
    try:
        fecha_hora = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print(
            f"[{fecha_hora}]"
            f"{Fore.GREEN}   Mensaje recibido{Style.RESET_ALL} | "
            f"Nombre: {Fore.YELLOW}{nombre}{Style.RESET_ALL} | "
            f"Número: {Fore.BLUE}{numero}{Style.RESET_ALL} | "
            f"Contenido: '{Fore.GREEN}{texto}{Style.RESET_ALL}' |"
        )
    except Exception as e:
        print(f"[{_ahora()}]{Fore.RED}   Error en mensaje_recibido(): {e}{Style.RESET_ALL}")


# --- Mensaje enviado ---
def mensaje_log_enviado(numero, texto):
    try:
        print(
            f"[{_ahora()}]"
            f"{Fore.CYAN}   Mensaje enviado{Style.RESET_ALL} | "
            f"Para: {Fore.BLUE}{numero}{Style.RESET_ALL} | "
            f"Contenido: {Fore.GREEN}'{texto}'{Style.RESET_ALL} |"
        )
    except Exception as e:
        print(f"[{_ahora()}]{Fore.RED}   Error en mensaje_enviado(): {e}{Style.RESET_ALL}")


# --- Usuario agregado ---
def mensaje_log_usuario_agregado(numero, nombre):
    try:
        print(
            f"[{_ahora()}]"
            f"{Fore.MAGENTA}   Nuevo usuario agregado{Style.RESET_ALL} | "
            f"Nombre: {Fore.YELLOW}{nombre}{Style.RESET_ALL} | Número: {Fore.BLUE}{numero}{Style.RESET_ALL} |"
        )
    except Exception as e:
        print(f"[{_ahora()}]{Fore.RED}   Error en mensaje_log_usuario_agregado(): {e}{Style.RESET_ALL}")


# --- Alerta ---
def mensaje_log_alerta(texto):
    print(f"[{_ahora()}]{Fore.YELLOW}   {texto}{Style.RESET_ALL}")


# --- Error ---
def mensaje_log_error(texto):
    try:
        print(f"[{_ahora()}]{Fore.RED}   {texto}{Style.RESET_ALL}")
    except Exception as e:
        print(f"[{_ahora()}]{Fore.RED}   Error en mensaje_log_error(): {e}{Style.RESET_ALL}")
