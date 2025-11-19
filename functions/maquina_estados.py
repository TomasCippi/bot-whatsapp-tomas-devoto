from functions.templates import *
from functions.mensajes_funciones import *
from functions.db_funciones import cambiar_estado_usuario

def procesar_flujo(numero_real, numero_hash, estado, mensaje_tipo, cuerpo_mensaje, interactive_id):
    """
    Máquina de estados centralizada.
    """
    
    # ===========================================================================
    # 🟢 ESTADO 0: MENÚ PRINCIPAL
    # ===========================================================================
    if estado == 0:
        
        if mensaje_tipo == "interactive":
            
            # --- OPCIONES INFORMATIVAS (NO CAMBIAN ESTADO) ---
            if interactive_id == "menu_principal_opt1":   # Sobre nosotros
                template_sobre_nosotros(numero_real)
                return

            elif interactive_id == "menu_principal_opt5": # Contacto
                template_contacto(numero_real)
                return

            elif interactive_id == "menu_principal_opt6": # Inscripciones
                # Como no tenías template para esto, mando un genérico y el menú de nuevo
                mensaje_texto(numero_real, "📩 Para inscripciones, por favor escribinos a info@tomasdevoto.edu.ar")
                template_menu_principal(numero_real, "¿En qué más te puedo ayudar?")
                return

            # --- OPCIONES DE NAVEGACIÓN (SÍ CAMBIAN ESTADO) ---
            elif interactive_id == "menu_principal_opt2": # Nivel Inicial
                cambiar_estado_usuario(numero_hash, 2.1)
                template_nivel_inicial(numero_real)
                return

            elif interactive_id == "menu_principal_opt3": # Nivel Primario
                cambiar_estado_usuario(numero_hash, 2.2)
                template_nivel_primario(numero_real)
                return

            elif interactive_id == "menu_principal_opt4": # Nivel Secundario
                cambiar_estado_usuario(numero_hash, 2.3)
                template_nivel_secundario(numero_real)
                return

        # Si no es botón o el ID no coincide, mostramos error suave
        template_menu_principal_error(numero_real, "Principal")
        template_menu_principal(numero_real, "Por favor, elige una opción del menú:")


    # ===========================================================================
    # 🔵 ESTADO 2.1: NIVEL INICIAL
    # ===========================================================================
    elif estado == 2.1:
        if interactive_id == "menu_nivel_inicial_opt5": # Volver
            cambiar_estado_usuario(numero_hash, 0)
            template_menu_principal(numero_real, "Menú Principal")
            return

        mapa = {
            "menu_nivel_inicial_opt1": template_n_i_propuestas_pedagogicas,
            "menu_nivel_inicial_opt2": template_n_i_talleres_optativos,
            "menu_nivel_inicial_opt3": template_n_i_servicios_adicionales,
            "menu_nivel_inicial_opt4": template_n_i_horarios
        }

        if interactive_id in mapa:
            mapa[interactive_id](numero_real)
        else:
            template_menu_principal_error(numero_real, "Nivel Inicial")
            template_menu_nivel_inicial(numero_real, "¿Qué deseas saber?")


    # ===========================================================================
    # 🟠 ESTADO 2.2: NIVEL PRIMARIO
    # ===========================================================================
    elif estado == 2.2:
        if interactive_id == "menu_nivel_primario_opt6": # Volver
            cambiar_estado_usuario(numero_hash, 0)
            template_menu_principal(numero_real, "Menú Principal")
            return
            
        mapa = {
            "menu_nivel_primario_opt1": template_n_p_propuestas_pedagogicas,
            "menu_nivel_primario_opt2": template_n_p_talleres_optativos,
            "menu_nivel_primario_opt3": template_n_p_algunos_proyectos,
            "menu_nivel_primario_opt4": template_n_p_servicios_adicionales,
            "menu_nivel_primario_opt5": template_n_p_horarios
        }

        if interactive_id in mapa:
            mapa[interactive_id](numero_real)
        else:
            template_menu_principal_error(numero_real, "Nivel Primario")
            template_menu_nivel_primario(numero_real, "¿Qué deseas saber?")
            

    # ===========================================================================
    # 🔴 ESTADO 2.3: NIVEL SECUNDARIO
    # ===========================================================================
    elif estado == 2.3:
        if interactive_id == "menu_nivel_secundario_opt5": # Volver
            cambiar_estado_usuario(numero_hash, 0)
            template_menu_principal(numero_real, "Menú Principal")
            return
            
        mapa = {
            "menu_nivel_secundario_opt1": template_n_s_propuestas_pedagogicas,
            "menu_nivel_secundario_opt2": templae_n_s_algunos_proyectos,
            "menu_nivel_secundario_opt3": template_n_s_planes_estudio,
            "menu_nivel_secundario_opt4": template_n_s_horarios
        }

        if interactive_id in mapa:
            mapa[interactive_id](numero_real)
        else:
            template_menu_principal_error(numero_real, "Nivel Secundario")
            template_menu_nivel_secundario(numero_real, "¿Qué deseas saber?")

    else:
        # Si el estado no existe (ej. null), lo forzamos a 0 silenciosamente 
        # sin mandarle mensajes de error al usuario.
        cambiar_estado_usuario(numero_hash, 0)
        template_menu_principal(numero_real, "Hola! En qué te puedo ayudar?")