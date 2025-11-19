import random
from functions.mensajes_funciones import *

# --------------------------- Mensajes de bienvenida --------------------------- #
def template_bienvenida(numero: str, nombre: str):
    mensaje_texto(numero, f"¡Hola *{nombre}*! 👋 Bienvenido/a al bot del *Tomas Devoto*. Estamos felices de que nos escribas 😃.")
    mensaje_texto(numero, "🎯 Este bot funciona a *través de menús* y *solo responde los mensajes que aparecen como opciones o los que te indique*. ¡Sigue las instrucciones y será muy fácil de usar!")   
    template_menu_principal(numero, "En que te puedo ayudar hoy?")

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

    template_menu_principal(numero, "En que te puedo ayudar hoy?")

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

# --------------------------- Mensajes de error --------------------------- #
def template_menu_principal_error(numero: str, menu_texto: str):
    mensaje_texto(numero, f"🤒 Ups! no entendí tu respuesta. El bot solo interpreta las respuestas de los menus, elige una opcion del menu *{menu_texto}* para continuar")

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

    template_menu_nivel_inicial(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Inicial*?")

# --------------------------- Mensajes sobre nivel primario 📙 --------------------------- #
def template_menu_nivel_primario(numero: str, texto: str):
    botones = [
        {"id": "menu_nivel_primario_opt1", "title": "Propuestas pedagógicas 💡"},
        {"id": "menu_nivel_primario_opt2", "title": "Talleres optativos 🎨"},
        {"id": "menu_nivel_primario_opt3", "title": "Algunos proyectos 🛠️"},
        {"id": "menu_nivel_primario_opt4", "title": "Servicios adicionales 🧩"},
        {"id": "menu_nivel_primario_opt5", "title": "Horarios 🕒"},
        {"id": "menu_nivel_primario_opt6", "title": "Menu anterior 🔙"}
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

def template_nivel_primario(numero: str):
    mensaje_texto(numero, "¡Buenísimo! Te contaré un poco sobre nuestro *Nivel Primario* 😆📙")

    mensaje_texto(numero, "📌 En *Nivel Primario*, nuestro propósito es que nuestros alumnos y alumnas crezcan y aprendan en un ambiente *rico en experiencias* que inviten a descubrir el mundo interactuando con otros en una *saludable convivencia*.")

    mensaje_texto(numero, "✉️ Para más información o consultas, podés escribirnos a *secretaria.primaria@tomasdevoto.edu.ar* o visitar nuestra web *https://tomasdevoto.edu.ar/nivel_primario/*")

    template_menu_nivel_primario(numero, "Qué te gustaría saber sobre el *Nivel Primario*?")

def template_n_p_propuestas_pedagogicas(numero:str):
    mensaje_texto(numero, "💡 Nuestras *propuestas pedagógicas* son las siguientes:")
    
    mensaje_texto(numero,"""
🇮🇹🇬🇧 *Italiano e Inglés*: El italiano es nuestro idioma distintivo y se enseña de 1º a 7º grado, integrando cultura, tradiciones y valores de Italia mediante canciones, juegos, cuentos y material audiovisual.
El inglés se ofrece como segundo idioma y puede reforzarse con talleres extracurriculares dos veces por semana en horario de la tarde.

🏐 *Educación Física*: Se realizan dos jornadas obligatorias los miércoles y viernes en el campo de deportes del Club Ferrocarril Gral. Mitre. El objetivo es jugar, moverse, aprender destrezas motoras y compartir actividades deportivas y recreativas con los compañeros. Esta experiencia intensificada se mantiene durante los siete años del nivel y da identidad a la escuela.

💻 *Educación Tecnológica y Digital*: Se fomenta la comprensión crítica y creativa de la tecnología y el uso de herramientas digitales
- *Tecnología*: Permite interrogarse sobre el pasado, presente y futuro tecnológico y el rol del ciudadano en su desarrollo.

- *Informática*: Promueve autonomía en el manejo de la computadora, selección de información, interpretación de contenidos y elaboración de trabajos escolares.

🎨 *Educación Artística*: Se busca que los alumnos profundicen en distintos lenguajes artísticos para conocerlos, disfrutarlos y comprenderlos
- *Música*: Aprender y crear música de manera activa, participativa y placentera.

- *Plástica*: Explorar el universo visual y comprender su relevancia en la vida cotidiana.

- *Teatro*: Desarrollar imaginación, expresividad corporal y vocal, y usar el lenguaje teatral como medio de comunicación.
""")

    template_menu_nivel_primario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Primario*?")

def template_n_p_talleres_optativos(numero: str):
    mensaje_texto(numero, "🎨 Algunos de nuestros *talleres optativos* son:")

    mensaje_texto(numero, """
🖌️ *Taller de Arte*: Un espacio para disfrutar y crear, estimulando la creatividad, la percepción, la sensibilidad y la expresión. Fomenta la autonomía y la autogestión, potenciando el desarrollo integral de la personalidad de los alumnos.

🥋 *Taller de Taekwondo*: Dictado por la tarde, enseña disciplina, autocontrol y respeto mutuo, promoviendo conductas no violentas y fortaleciendo valores personales.

🇬🇧 *Certificación y Taller de Inglés*: El Instituto Tomas Devoto, en convenio con la UTN, ofrece certificación oficial de inglés con validez nacional. Además, se ofrece un taller optativo y extracurricular, dinámico y divertido, donde los alumnos aprenden inglés jugando, cantando, leyendo cuentos y dramatizando. El taller promueve autodisciplina, creatividad y respeto a las diferencias, y acompaña a los alumnos desde nivel inicial hasta secundaria.
""")

    template_menu_nivel_primario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Primario*?")

def template_n_p_algunos_proyectos(numero: str):
    mensaje_texto(numero, "🛠️ Algunos *proyectos* que hicimos:")

    mensaje_texto(numero, """
🤝 *Proyecto Padrinos y Ahijados*: Los alumnos de 7° acompañan a los de 1° durante el año, compartiendo juegos, recreos, clases y actividades especiales, generando vínculos de confianza y afecto entre los más grandes y los recién ingresados.

📚 *Animación a la Lectura*: Promovemos el disfrute de la lectura y la participación en la comunidad de lectores, fomentando la reflexión, la búsqueda de información y la expresión de emociones y sensaciones a través de la literatura.

👐 *Proyectos Solidarios Comunitarios*: Enseñamos la solidaridad como valor cotidiano. Colaboramos con la escuela N° 442 de Catamarca y estamos abiertos a nuevas campañas y experiencias comunitarias, ayudando con compromiso y afecto.

🌸 *Proyecto ESI (Educación Sexual Integral)*: La ESI se integra en todas las áreas para desarrollar empatía, expresión de emociones y respeto. La participación familiar es clave para garantizar derechos de información y expresión en un entorno pluralista.

🏆 *Juegos Interbandos*: Los bandos blanco, rojo y verde compiten en juegos y desafíos durante todo el año. Familias y estudiantes celebran juntos, fomentando compañerismo, esfuerzo y espíritu deportivo.

⛺ *Campamentos*: La vida en la naturaleza enseña cuidado del medio ambiente y convivencia. Desde 1° hasta 7°, los alumnos disfrutan de juegos, canciones, fogones y contacto directo con ríos, sierras, animales y plantas, generando experiencias únicas de aprendizaje.
""")

    template_menu_nivel_primario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Primario*?")

def template_n_p_servicios_adicionales(numero: str):
    mensaje_texto(numero, "🧩 Algunos *servicios adicionales* que tenemos:")

    mensaje_texto(numero, """
*🍽️ Comedor*: Nuestro comedor ofrece comidas nutritivas y deliciosas para que disfrutes tus días en la escuela. ¡Buen provecho!

*🚌 Transporte*: Contamos con transporte seguro y cómodo para que llegues y vuelvas a casa sin preocupaciones. ¡Viaja tranquilo!
""")

    template_menu_nivel_primario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Primario*?")

def template_n_p_horarios(numero: str):
    mensaje_texto(numero, "🕒 Los *horarios* son los siguientes:")

    mensaje_texto(numero, """
*Turno mañana*:

*Ingreso*: 7:30 a 7:40hs
de lunes a viernes. ( 1ro a 7mo grado)

*Salida*: 12:30hs
de lunes a viernes.(1ro y 2do grado).

*3ro a 7mo prolongación horaria de inglés hasta las 13:30hs*
(3er grado una vez a la semana, 4to a 7mo grado , dos veces por semana).

*Turno tarde*:
*Lunes, martes y jueves de 14 a 17 horas*
Talleres optativos extraprogramáticos.

*Miércoles y viernes de 14 a 17 horas*
Taller de educación física en campo de deportes (modalidad obligatoria).
""")

    template_menu_nivel_primario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Primario*?")

# --------------------------- Mensajes sobre nivel secundario 📕 --------------------------- #
def template_menu_nivel_secundario(numero: str, texto: str):
    botones = [
        {"id": "menu_nivel_secundario_opt1", "title": "Propuestas pedagógicas 💡"},
        {"id": "menu_nivel_secundario_opt2", "title": "Algunos proyectos 🧩"},
        {"id": "menu_nivel_secundario_opt3", "title": "Planes de estudio 📝"},
        {"id": "menu_nivel_secundario_opt4", "title": "Horarios 🕒"},
        {"id": "menu_nivel_secundario_opt5", "title": "Menu anterior 🔙"}
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

def template_nivel_secundario(numero: str):
    mensaje_texto(numero, "¡Genial! Te contaré un poco sobre nuestro *Nivel Secundario* 😆📕")

    mensaje_texto(numero, "📌 En *Nivel Secundario* buscamos el desarrollo integral de los alumnos, fomentando *autonomía, resiliencia y libertad responsable*, para que puedan valorar lo verdadero y bueno, y convertirse en agentes de cambio positivo en su comunidad.")

    mensaje_texto(numero, "✉️ Para más información o consultas, podés escribirnos a *secretaria.secundario@tomasdevoto.edu.ar* o visitar nuestra web *https://tomasdevoto.edu.ar/nivel-secundario/*")

    template_menu_nivel_secundario(numero, "Qué te gustaría saber sobre el *Nivel Secundario*?")

def template_n_s_propuestas_pedagogicas(numero:str):
    mensaje_texto(numero, "💡 Nuestras *propuestas pedagógicas* son las siguientes:")

    mensaje_texto(numero, """
💬 *Bachiller en Comunicación*:
Forma a los y las estudiantes en la interpretación y producción de procesos comunicacionales. Aborda las dimensiones interpersonales, institucionales y comunitarias desde una perspectiva intercultural y multimedial. Integra saberes de las ciencias sociales (filosofía, historia, sociología, economía, política, psicología, etc.) para comprender y producir prácticas comunicativas.
*Bloques*:
- Estudios de la comunicación
- Producción en lenguajes multimediales
- Saberes y prácticas en comunicación

📈 *Bachiller en Economía y Administración*:
Brinda herramientas para analizar fenómenos sociales, económicos y organizacionales. Estudia el funcionamiento del sistema económico, los agentes intervinientes, el rol del Estado y los modelos de desarrollo. Promueve la reflexión sobre el impacto social, político, ambiental y cultural de la actividad económica y organizacional.
*Bloques*:
- Economía y administración de organizaciones
- Sistemas de información organizacional
- Regulación de la actividad económica
""")
    
    mensaje_texto(numero,"""
🗣️ *Lenguas Adicionales (Italiano e Inglés)*: Permiten conocer los fenómenos del lenguaje humano y acceder a distintas culturas. A través del contraste con la lengua materna, promueven la reflexión sobre la diversidad y la alteridad. Su enseñanza se organiza en torno a prácticas sociales del lenguaje.

🏃‍♂️ *Educación Física y Deportes*: Favorece el desarrollo corporal, lúdico y motor, promoviendo salud, autoestima y conciencia del cuidado propio y del entorno. Incluye prácticas deportivas, expresivas y recreativas, reconociendo su valor social y formativo. Intensificación profundiza en la participación de deportes como:
- handball
- voleibol 
- hockey  
- atletismo 
fomentando valores como solidaridad, cooperación y compromiso.

🎨 *Artes*: Ofrece experiencias de creación, apreciación y reflexión artística, desarrollando la expresión, la sensibilidad y la capacidad de análisis.

💻 *Campus Virtual / Plataforma Educativa*: Espacio digital que acompaña las distintas materias, favoreciendo el trabajo colaborativo y el aprendizaje en línea.
""")

    template_menu_nivel_secundario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Secundario*?")

def templae_n_s_algunos_proyectos(numero: str):
    mensaje_texto(numero, "🧩 *Algunos proyectos*:")

    mensaje_texto(numero, """
*📚 Educación Sexual Integral (ESI)*: La ESI se enseña de manera sistemática en todos los niveles de la CABA, garantizando derechos, igualdad de acceso a la información y formación, y cumpliendo la ley Nº 2110/06. Aborda la sexualidad de forma integral: psicológica, ética, biológica, jurídica, sociocultural, histórica y de salud. Se aplica mediante:
- Contenidos transversales en distintas materias.
- Jornadas ESI según la Agenda Educativa de la Ciudad.
- Situaciones emergentes del día a día.
- Talleres y espacios curriculares específicos (ECEO) participativos.

*🌳 Salidas Educativas al Medio*: Las salidas al medio ofrecen experiencias pedagógicas únicas, usando distintos escenarios y recursos. Potencian la observación, interpretación y reflexión del entorno social del estudiantado. Durante la secundaria, se realizan dentro de proyectos institucionales, interdisciplinarios y espacios curriculares específicos.

*🚌 Viajes Educativos*: Los viajes educativos permiten conocer nuevos lugares, su historia y cultura, enriquecen los aprendizajes y fortalecen los vínculos del grupo, acercando a los estudiantes a distintos contenidos de manera vivencial.

*🤾 Juegos Deportivos Interbandos*: Estas actividades combinan ejercicio físico y trabajo cooperativo, desarrollando habilidades físicas y sociales, y fomentando una educación en valores a través del deporte.

*🇮🇹 Giochi della Gioventù*: Desde 1984, estos juegos fomentan la práctica deportiva y el crecimiento social en jóvenes de la colectividad italiana y de Sudamérica. Se realizan en Buenos Aires durante 3 días, con más de 4.500 participantes compitiendo en deportes como atletismo, básquet, fútbol, handball, hockey, natación, tenis y vóleibol. Nuestra escuela participa cada año.

*📻 Radio (Comunicación)*: Los estudiantes de quinto año participan en talleres de radio, crean programas temáticos y se emiten por Radio Monk, aprendiendo a trabajar en equipo y compartir responsabilidades.

*💼 Emprendedurismo (Economía)*: Alumnos de 4º y 5º año desarrollan proyectos de emprendedurismo creando y gestionando su propia empresa con compromiso ambiental, aplicando conocimientos de la escuela y reflexionando sobre la gestión responsable y el impacto social y económico.
""")

    template_menu_nivel_secundario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Secundario*?")

def template_n_s_planes_estudio(numero: str):
    mensaje_texto(numero, "📝 Estos son nuestros *planes de estudio*:")

    mensaje_imagen(numero, "861325292982411", "Plan de estudio *ECONOMIA*")

    mensaje_imagen(numero, "25348420904771189", "Plan de estudio *COMUNICACION*")

    template_menu_nivel_secundario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Secundario*?")

def template_n_s_horarios(numero: str):
    mensaje_texto(numero, "🕒 Los *horarios* son los siguientes:")

    mensaje_texto(numero, """
*Turno mañana*:
Lunes a viernes   -   7:20hs/13:20hs

*Turno tarde*:
Educación Física y Deportes   -   Voley, Handball, Atletismo y Hockey.
Lunes y Jueves o Martes y Jueves   -   entre las 14:00 hs. y las 18:00 hs.
""")

    template_menu_nivel_secundario(numero, "Qué otra cosa te gustaría saber sobre el *Nivel Secundario*?")