from flask import Flask, request
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta

from functions.verificar_webhook import verificar_webhook
from functions.consola_logs import *
from functions.db_funciones import *
from functions.templates import *

load_dotenv()
app = Flask(__name__)

# ------------------- LOGS ------------------- #
def imprimir_logs():
    if os.getenv("IMPRIMIR_LOGS_FLASK") == "True":
        print("🟢 Logs de Flask activos")
    else:
        import logging
        logging.getLogger('werkzeug').disabled = True
        app.logger.disabled = True
        print("🛑 Logs de Flask desactivados")

# ------------------- WEBHOOK ------------------- #
@app.route("/webhook", methods=["GET"])
def verificar():
    return verificar_webhook()


@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    try:
        data = request.json
        cambio = data.get("entry", [])[0].get("changes", [])[0].get("value", {})

        if "messages" not in cambio:
            return "EVENT_RECEIVED", 200

        mensaje = cambio["messages"][0]
        tipo = mensaje.get("type")
        contacto = cambio["contacts"][0]
        nombre = contacto["profile"].get("name", "Desconocido")

        # ⚠️ IMPORTANTE: reemplazar cuando termines debug
        numero_real = "541158633864"
        
        numero_hash = hash_numero(numero_real)
        timestamp = mensaje.get("timestamp", "0")

        # ------------------- TEXTO / INTERACTIVO ------------------- #
        if tipo == "text":
            texto = mensaje["text"]["body"]

        elif tipo == "interactive":
            interactivo = mensaje["interactive"]
            if "list_reply" in interactivo:
                titulo = interactivo["list_reply"]["title"]
                menu_id = interactivo["list_reply"]["id"]
                texto = f"{titulo} [MENU {menu_id}]"
            elif "button_reply" in interactivo:
                titulo = interactivo["button_reply"]["title"]
                menu_id = interactivo["button_reply"]["id"]
                texto = f"{titulo} [BOTON {menu_id}]"
            else:
                texto = "[INTERACTIVO DESCONOCIDO]"
        else:
            texto = f"[{tipo.upper()}]"

        # ------------------- BLACKLIST ------------------- #
        if numero_en_blacklist(numero_hash):
            return "EVENT_RECEIVED", 200

        mensaje_log_recibido(nombre, numero_real, texto, timestamp)

        # ------------------- USUARIO NUEVO ------------------- #
        if not verificar_numero(numero_hash):
            if insertar_usuario(numero_hash, nombre):
                mensaje_log_usuario_agregado(numero_real, nombre)
                cambiar_estado_usuario(numero_hash, 0)
                template_bienvenida(numero_real, nombre)

                # Registrar último mensaje enviado
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users 
                        SET ultimo_mensaje_enviado = %s 
                        WHERE numero = %s;
                    """, (datetime.now(), numero_hash))
                    conn.commit()
                    conn.close()

                return "EVENT_RECEIVED", 200

            else:
                mensaje_log_error(f"No se pudo insertar {numero_real}")
                return "EVENT_RECEIVED", 200

        # ------------------- CONTROL DE 5 HORAS ------------------- #
        control_ultimo_mensaje(numero_hash)

        # ------------------- ESTADO ACTUAL ------------------- #
        estado = obtener_estado_usuario(numero_hash)
        if estado is None:
            cambiar_estado_usuario(numero_hash, 0)
            estado = 0

        # ------------------- MÁQUINA DE ESTADOS ------------------- #

        # === ESTADO 0 → MENÚ PRINCIPAL === #
        if estado == 0:

            if tipo == "interactive":
                interactivo = mensaje.get("interactive", {})
                menu_id = None

                if "list_reply" in interactivo:
                    menu_id = interactivo["list_reply"]["id"]
                elif "button_reply" in interactivo:
                    menu_id = interactivo["button_reply"]["id"]

                mapa_principal = {
                    "menu_principal_opt1": (1, lambda n: template_sobre_nosotros(n)),
                    "menu_principal_opt2": (2.1, lambda n: template_nivel_inicial(n)),
                    "menu_principal_opt3": (2.2, lambda n: template_nivel_primario(n)),
                    "menu_principal_opt4": (2.3, lambda n: template_nivel_secundario(n)),
                    "menu_principal_opt5": (5, lambda n: template_contacto(n)),
                    "menu_principal_opt6": (6, lambda n: None)
                }

                if menu_id in mapa_principal:
                    nuevo_estado, funcion = mapa_principal[menu_id]
                    cambiar_estado_usuario(numero_hash, nuevo_estado)
                    funcion(numero_real)
                    return "EVENT_RECEIVED", 200

            # ❌ error menú principal
            template_menu_principal_error(numero_real, "Principal")
            template_menu_principal(numero_real, "Elige una opción del menú principal")
            return "EVENT_RECEIVED", 200



        # === ESTADO 2.1 → MENÚ NIVEL INICIAL === #
        elif estado == 2.1:

            if tipo == "interactive":
                interactivo = mensaje.get("interactive", {})
                menu_id = None

                if "list_reply" in interactivo:
                    menu_id = interactivo["list_reply"]["id"]
                elif "button_reply" in interactivo:
                    menu_id = interactivo["button_reply"]["id"]

                mapa_inicial = {
                    "menu_nivel_inicial_opt1": lambda n: template_n_i_propuestas_pedagogicas(n),
                    "menu_nivel_inicial_opt2": lambda n: template_n_i_talleres_optativos(n),
                    "menu_nivel_inicial_opt3": lambda n: template_n_i_servicios_adicionales(n),
                    "menu_nivel_inicial_opt4": lambda n: template_n_i_horarios(n),
                    "menu_nivel_inicial_opt5": "volver"
                }

                if menu_id in mapa_inicial:

                    if mapa_inicial[menu_id] == "volver":
                        cambiar_estado_usuario(numero_hash, 0)
                        template_menu_principal(numero_real, "Volvemos al menú principal")
                    else:
                        mapa_inicial[menu_id](numero_real)

                    return "EVENT_RECEIVED", 200

            # ❌ error nivel inicial
            template_menu_principal_error(numero_real, "Nivel Inicial")
            template_menu_nivel_inicial(numero_real, "Elegí una opción válida del Nivel Inicial")
            return "EVENT_RECEIVED", 200



        # === ESTADO 2.2 → MENÚ NIVEL PRIMARIO === #
        elif estado == 2.2:

            if tipo == "interactive":
                interactivo = mensaje.get("interactive", {})
                menu_id = None

                if "list_reply" in interactivo:
                    menu_id = interactivo["list_reply"]["id"]
                elif "button_reply" in interactivo:
                    menu_id = interactivo["button_reply"]["id"]

                mapa_primario = {
                    "menu_nivel_primario_opt1": lambda n: template_n_p_propuestas_pedagogicas(n),
                    "menu_nivel_primario_opt2": lambda n: template_n_p_talleres_optativos(n),
                    "menu_nivel_primario_opt3": lambda n: template_n_p_algunos_proyectos(n),
                    "menu_nivel_primario_opt4": lambda n: template_n_p_servicios_adicionales(n),
                    "menu_nivel_primario_opt5": lambda n: template_n_p_horarios(n),
                    "menu_nivel_primario_opt6": "volver"
                }

                if menu_id in mapa_primario:

                    if mapa_primario[menu_id] == "volver":
                        cambiar_estado_usuario(numero_hash, 0)
                        template_menu_principal(numero_real, "Volvemos al menú principal")
                    else:
                        mapa_primario[menu_id](numero_real)

                    return "EVENT_RECEIVED", 200

            # ❌ error nivel primario
            template_menu_principal_error(numero_real, "Nivel Primario")
            template_menu_nivel_primario(numero_real, "Elegí una opción válida del Nivel Primario")
            return "EVENT_RECEIVED", 200



        # === ESTADO 2.3 → MENÚ NIVEL SECUNDARIO === #
        elif estado == 2.3:

            if tipo == "interactive":
                interactivo = mensaje.get("interactive", {})
                menu_id = None

                if "list_reply" in interactivo:
                    menu_id = interactivo["list_reply"]["id"]
                elif "button_reply" in interactivo:
                    menu_id = interactivo["button_reply"]["id"]

                mapa_secundario = {
                    "menu_nivel_secundario_opt1": lambda n: template_n_s_propuestas_pedagogicas(n),
                    "menu_nivel_secundario_opt2": lambda n: templae_n_s_algunos_proyectos(n),  # Respeto tu nombre
                    "menu_nivel_secundario_opt3": lambda n: template_n_s_planes_estudio(n),
                    "menu_nivel_secundario_opt4": lambda n: template_n_s_horarios(n),
                    "menu_nivel_secundario_opt5": "volver"
                }

                if menu_id in mapa_secundario:

                    if mapa_secundario[menu_id] == "volver":
                        cambiar_estado_usuario(numero_hash, 0)
                        template_menu_principal(numero_real, "Volvemos al menú principal")
                    else:
                        mapa_secundario[menu_id](numero_real)

                    return "EVENT_RECEIVED", 200

            # ❌ error nivel secundario
            template_menu_principal_error(numero_real, "Nivel Secundario")
            template_menu_nivel_secundario(numero_real, "Elegí una opción válida del Nivel Secundario")
            return "EVENT_RECEIVED", 200


    except Exception as e:
        mensaje_log_error(f"Error procesando mensaje: {e}")

    return "EVENT_RECEIVED", 200


# ------------------- MAIN ------------------- #
if __name__ == "__main__":
    limpiar_usuarios()  # modo test
    imprimir_logs()
    app.run(debug=True, port=5000)
