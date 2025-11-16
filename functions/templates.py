import random
from functions.mensajes_funciones import *

# --------------------------- Mensajes de bienvenida --------------------------- #
def template_bienvenida(numero: str, nombre: str):
    mensaje_texto(numero, f"¡Hola *{nombre}*! 👋 Bienvenido/a al bot del *Tomas Devoto*. Estamos felices de que nos escribas 😃.")
    mensaje_texto(numero, "🎯 Este bot funciona a *través de menús* y *solo responde los mensajes que aparecen como opciones o los que te indique*. ¡Sigue las instrucciones y será muy fácil de usar!")   

def template_bienvenida_devuelta(numero: str, nombre: str):
    mini_mensajes = [
        "Esperamos que tengas un día increíble 😃",
        "Qué bueno verte otra vez por aquí 👋",
        "Nos alegra verte de nuevo 😆"
    ]
    # Elegir uno al azar
    mensaje_aleatorio = random.choice(mini_mensajes)
    # Mensaje completo combinado
    mensaje_completo = f"¡Bienvenido/a otra vez, *{nombre}*! {mensaje_aleatorio}"

    mensaje_texto(numero, mensaje_completo)

# --------------------------- Mensajes principales --------------------------- #
def template_menu_principal(numero: str, texto: str):
    botones = [
        {"id": "menu_principal_opt1", "title": "Sobre nosotros 🏫"},
        {"id": "menu_principal_opt2", "title": "Nivel inicial 📘"},
        {"id": "menu_principal_opt3", "title": "Nivel primario 📙"},
        {"id": "menu_principal_opt4", "title": "Nivel secundario 📕"},
        {"id": "menu_principal_opt5", "title": "Contacto 💬"},
        {"id": "menu_principal_opt6", "title": "Inscripciones 📩"}
    ]

    # Enviar lista interactiva
    mensaje_lista(
        numero=numero,
        titulo="Opciones",
        texto=texto,
        footer="",
        botones=botones,
        menu_id="menu_principal"
    )

def template_menu_error(numero: str, menu_id: str):
    mensaje_texto(numero, f"🤒 Ups! no entendí tu respuesta. Por favor, solo elige una opción del menú *{menu_id}* para continuar")

# --------------------------- Mensajes sobre nosotros 🏫 --------------------------- #
def template_sobre_nosotros(numero: str):
    mensaje_texto(numero, "Claro! Te contaré un poco sobre el *Tomás Devoto* 😄🏫.")
    mensaje_texto(numero, "🎯 Nuestra misión es acompañar a nuestros alumnos en su desarrollo integral, formando personas autónomas, responsables y conscientes, capaces de construir su propio camino y de generar un impacto positivo en su comunidad.")

    mensaje_texto(numero, """En el *Tomas Devoto* contamos con:

🏥 *Departamento médico*: que se encarga de la salud de nuestros estudiantes, ofreciendo atención básica y apoyo en casos de emergencias o consultas médicas.
👩‍🏫 *Equipo de orientación*:que acompaña a cada alumno, brindando asesoramiento académico y apoyo emocional, ayudándolos a superar dificultades y a tomar decisiones que favorezcan su desarrollo personal y educativo.
    """)

    mensaje_texto(numero, "📍 El *Tomas Devoto* se ubica en *Villa Urquiza*, en *Franklin D. Roosevelt 5678*")

    template_menu_principal(numero, "En que otra cosa podemos ayudarte hoy?")

# --------------------------- Mensajes sobre contacto 💬 --------------------------- #
def template_contacto(numero:str):
    mensaje_texto(numero, "¡Por supuesto! Estas son las formas en las que puedes contactarnos 😃💬.")

    mensaje_texto(numero, """✉️ Por *mail*:

*Información General*:
info@tomasdevoto.edu.ar
*Nivel Inicial*:
secretaria.inicial@tomasdevoto.edu.ar
*Nivel Primario*:
secretaria.primaria@tomasdevoto.edu.ar
*Nivel Secundario*: 
secretaria.secundario@tomasdevoto.edu.ar

📞 Por *telefono*:
(011) 4571-2019   
""")

    mensaje_texto(numero, "¡Si nos escribes, nos contactaremos contigo lo antes posible!")

    mensaje_texto(numero, "🌐 Si quieres conocer más información, puedes visitar nuestra página web: https://tomasdevoto.edu.ar/")
    
    mensaje_texto(numero, """
📱 Para estar al día con nuestras novedades, síguenos en nuestras redes sociales!:
*Instagram*:
https://www.instagram.com/institutotomasdevoto/
*YouTube*:
http://www.youtube.com/@itdstreaming
""")

    template_menu_principal(numero, "En que otra cosa podemos ayudarte hoy?")

# --------------------------- Mensajes sobre nivel inicial 📘 --------------------------- #

def template_menu_nivel_inicial(numero: str, texto: str):
    botones = [
        {"id": "menu_nivel_inicial_opt1", "title": "Propuestas pedagógicas 💡"},
        {"id": "menu_nivel_inicial_opt2", "title": "Talleres optativos 🎨"},
        {"id": "menu_nivel_inicial_opt3", "title": "Servicios adicionales 🧩"},
        {"id": "menu_nivel_inicial_opt4", "title": "Horarios 🕒"},
        {"id": "menu_nivel_inicial_opt5", "title": "Menu anterior 🔙"}
    ]

    # Enviar lista interactiva
    mensaje_lista(
        numero=numero,
        titulo="Opciones",
        texto=texto,
        footer="",
        botones=botones,
        menu_id="menu_principal"
    )

def template_nivel_inicial(numero: str):
    mensaje_texto(numero, "¡Buenísimo! Te contaré un poco sobre nuestro *Nivel Inicial* 😆📘")

    mensaje_texto(numero, "📌 En *Nivel Inicial*, los chicos y chicas aprenden jugando en un ambiente afectuoso y seguro. Fomentamos *solidaridad, respeto y empatía*, mientras desarrollan sus habilidades sociales y emocionales de manera integral.")

    mensaje_texto(numero, "✉️ Para más información o consultas, podés escribirnos a *secretaria.inicial@tomasdevoto.edu.ar* o visitar nuestra web *https://tomasdevoto.edu.ar/nivel-inicial/*")

    template_menu_nivel_inicial(numero, "Qué te gustaría saber sobre el *Nivel Inicial*?")

def template_n_i_propuestas_pedagogicas(numero:str):
    mensaje_texto(numero, "💡 Nuestras *propuestas pedagógicas* son las siguientes:")
    
    mensaje_texto(numero,"""
🇮🇹 *Italiano*: Introducimos a los niños y niñas en la lengua italiana desde los 3 años mediante actividades lúdicas, literarias y musicales.

🤸 *Educación Física*: Desde los 2 años, los alumnos exploran y desarrollan su motricidad a través de propuestas de juego y descubrimiento.

💻 *Educación Digital*: Incorporamos recursos digitales para que los niños adquieran habilidades tecnológicas que acompañen su trayectoria escolar.

🎵 *Educación Musical*: Brindamos experiencias musicales que sensibilizan a los niños sobre el mundo sonoro, ampliando su repertorio cultural y fomentando el disfrute de la música.
""")

    template_menu_nivel_inicial(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Inicial*?")

def template_n_i_talleres_optativos(numero: str):
    mensaje_texto(numero, "🎨 Algunos de nuestros *talleres optativos* son:")

    mensaje_texto(numero, """
🖌️ *Taller de Artes Visuales*: Fomentamos el conocimiento artístico mediante diferentes recursos y técnicas, ofreciendo un espacio de juego y creatividad que permite desarrollar la expresión y comunicación personal.

🏃 *Taller de Expresión y Movimiento*: Los niños acceden a prácticas corporales que, a través del movimiento, les permiten explorar y conocer el mundo de diversas formas.

🏐 *Taller de Iniciación Deportiva*: Intensificamos la práctica deportiva para favorecer un desarrollo integral, con experiencias corporales y motrices que continuarán en el Nivel Primario.

🇬🇧 *Taller de Inglés (UTN – INSPT)*: Introducimos a los alumnos en el conocimiento del inglés mediante propuestas lúdicas.

🧩 *Taller de Recreación*: Los niños participan en actividades pedagógicas a través de juegos y situaciones recreativas, fomentando la diversión y el aprendizaje.

""")

    template_menu_nivel_inicial(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Inicial*?")

def template_n_i_servicios_adicionales(numero: str):
    mensaje_texto(numero, "🧩 Algunos *servicios adicionales* que tenemos:")

    mensaje_texto(numero, """
*🍽️ Comedor*: Nuestro comedor ofrece comidas nutritivas y deliciosas para que disfrutes tus días en la escuela. ¡Buen provecho!

*🚌 Transporte*: Contamos con transporte seguro y cómodo para que llegues y vuelvas a casa sin preocupaciones. ¡Viaja tranquilo!
""")

    template_menu_nivel_inicial(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Inicial*?")

def template_n_i_horarios(numero: str):
    mensaje_texto(numero, "🕒 Los *horarios* son los siguientes:")

    mensaje_texto(numero, """
*Turno mañana*:
Sala de *2 años/3 años*   -   8:30hs/12:15hs
Sala de *4 años/5 años*   -   8:30hs/12:30hs

*Turno tarde*:
Sala de *2 años/3 años*   -   13:20hs/16:55hs
""")