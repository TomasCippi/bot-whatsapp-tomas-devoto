import os
import re
from colorama import Fore, Style
from datetime import datetime

# ========================
#  CONFIG LOGS
# ========================
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def _clean_ansi(texto: str) -> str:
    return ANSI_RE.sub("", texto)

def _log_to_file(texto: str):
    fecha = datetime.now().strftime("%Y-%m-%d")
    archivo = os.path.join(LOG_DIR, f"{fecha}.log")
    texto_limpio = _clean_ansi(texto)

    with open(archivo, "a", encoding="utf-8") as f:
        f.write(texto_limpio + "\n")

def _print_and_save(texto: str):
    print(texto)
    _log_to_file(texto)

# ========================
# Helper general
# ========================
def _ahora():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ========================
# Mensaje recibido
# ========================
def mensaje_log_recibido(nombre, numero, texto, estado):
    try:
        texto_unilinea = " ".join(texto.splitlines())
        texto_corto = (texto_unilinea[:80] + " ......") if len(texto_unilinea) > 80 else texto_unilinea

        texto_final = (
            f"[{_ahora()}]"
            f"{Fore.GREEN}   Mensaje recibido{Style.RESET_ALL} | "
            f"Nombre: {Fore.YELLOW}{nombre}{Style.RESET_ALL} | "
            f"Estado: {Fore.MAGENTA}[{estado}]{Style.RESET_ALL} | "
            f"Número: {Fore.BLUE}{numero}{Style.RESET_ALL} | "
            f"Contenido: '{Fore.GREEN}{texto_corto}{Style.RESET_ALL}'"
        )

        _print_and_save(texto_final)

    except Exception as e:
        _print_and_save(f"[{_ahora()}]{Fore.RED}   Error en mensaje_recibido(): {e}{Style.RESET_ALL}")

# ========================
# Mensaje enviado
# ========================
def mensaje_log_enviado(numero, texto):
    try:
        texto_unilinea = " ".join(texto.splitlines())
        texto_corto = (texto_unilinea[:80] + " ......") if len(texto_unilinea) > 80 else texto_unilinea

        texto_final = (
            f"[{_ahora()}]"
            f"{Fore.CYAN}   Mensaje enviado{Style.RESET_ALL} | "
            f"Para: {Fore.BLUE}{numero}{Style.RESET_ALL} | "
            f"Contenido: {Fore.GREEN}'{texto_corto}'{Style.RESET_ALL}"
        )

        _print_and_save(texto_final)

    except Exception as e:
        _print_and_save(f"[{_ahora()}]{Fore.RED}   Error en mensaje_enviado(): {e}{Style.RESET_ALL}")

# ========================
# Usuario agregado
# ========================
def mensaje_log_usuario_agregado(numero, nombre):
    try:
        texto_final = (
            f"[{_ahora()}]"
            f"{Fore.MAGENTA}   Nuevo usuario agregado{Style.RESET_ALL} | "
            f"Nombre: {Fore.YELLOW}{nombre}{Style.RESET_ALL} | "
            f"Número: {Fore.BLUE}{numero}{Style.RESET_ALL} |"
        )

        _print_and_save(texto_final)

    except Exception as e:
        _print_and_save(f"[{_ahora()}]{Fore.RED}   Error en mensaje_log_usuario_agregado(): {e}{Style.RESET_ALL}")

# ========================
# Alerta
# ========================
def mensaje_log_alerta(texto):
    texto_final = f"[{_ahora()}]{Fore.YELLOW}   {texto}{Style.RESET_ALL}"
    _print_and_save(texto_final)

# ========================
# Error
# ========================
def mensaje_log_error(texto):
    try:
        texto_final = f"[{_ahora()}]{Fore.RED}   {texto}{Style.RESET_ALL}"
        _print_and_save(texto_final)
    except Exception as e:
        _print_and_save(f"[{_ahora()}]{Fore.RED}   Error en mensaje_log_error(): {e}{Style.RESET_ALL}")
