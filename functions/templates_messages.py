import random
from dotenv import load_dotenv
from colorama import Fore, Style
from .send_messages import *

def mensaje_prueba(number, name):
    contacto_mensaje(number)

# --------------------------- Mensajes de bienvenida --------------------------- #
opciones_menu_principal = [
        {"id": "main_menu_opt1", "title": "Sobre nosotros 🏫"},
        {"id": "main_menu_opt2", "title": "Nivel inicial 📘"},
        {"id": "main_menu_opt3", "title": "Nivel primario 📙"},
        {"id": "main_menu_opt4", "title": "Nivel secundario 📕"},
        {"id": "main_menu_opt5", "title": "Contacto 💬"},
        {"id": "main_menu_opt6", "title": "Inscripciones 📩"}
]

def bienvenida_mensaje(to_number:str, to_name):
    send_text_message(to_number, f"¡Hola *{to_name}*! 👋 Bienvenido/a al bot del *Tomas Devoto*. Estamos felices de que nos escribas 😃.")
    send_text_message(to_number, """
🎯 Este bot funciona a *través de menús* y *solo responde los mensajes que aparecen como opciones o los que te indique*. ¡Sigue las instrucciones y será muy fácil de usar!
""")
    body_text = "En qué podemos ayudarte hoy?"
    
    opciones = opciones = opciones_menu_principal
    
    send_menu_list(to_number, body_text, opciones)

def bienvenida_devuelta_mensaje(to_number:str, to_name):
    mini_mensajes = [
        "Esperamos que tengas un día increíble 😃",
        "Qué bueno verte otra vez por aquí 👋",
        "Nos alegra verte de nuevo 😆"
    ]
    
    # Elegir uno al azar
    mensaje_aleatorio = random.choice(mini_mensajes)
    
    # Mensaje completo combinado
    mensaje_completo = f"¡Bienvenido/a otra vez, *{to_name}*! {mensaje_aleatorio}"
    
    send_text_message(to_number, mensaje_completo)

    body_text = "En qué podemos ayudarte hoy?"
    
    opciones = opciones_menu_principal
    
    send_menu_list(to_number, body_text, opciones)

# --------------------------- Mensajes sobre nosotros --------------------------- #

def sobre_nosotros_mensaje(to_number: str):
    send_text_message(to_number, "Genial! 😄 Te contaré un poco sobre el *Tomás Devoto*")
    send_text_message(to_number, """
🎯 Nuestra misión es acompañar a nuestros alumnos en su desarrollo integral, formando personas autónomas, responsables y conscientes, capaces de construir su propio camino y de generar un impacto positivo en su comunidad."
""")
    send_text_message(to_number, """
                        En el *Tomas Devoto* contamos con:\n\n🏥 *Departamento médico*:\nque se encarga de la salud de nuestros estudiantes, ofreciendo atención básica y apoyo en casos de emergencias o consultas médicas\n\n👩‍🏫 *Equipo de orientación*:\nque acompaña a cada alumno, brindando asesoramiento académico y apoyo emocional, ayudándolos a superar dificultades y a tomar decisiones que favorezcan su desarrollo personal y educativo
                    """)
    send_text_message(to_number, "📍 El *Tomas Devoto* se ubica en *Villa Urquiza*, en *Franklin D. Roosevelt 5678*")

    body_text = "En que otra cosa podemos ayudarte hoy?"
    
    opciones = opciones_menu_principal
    
    send_menu_list(to_number, body_text, opciones)

# --------------------------- Mensajes sobre contacto --------------------------- #

def contacto_mensaje(to_number:str):
    send_text_message(to_number, "¡Por supuesto! 😃 Estas son las formas en las que puedes contactarnos:")
    send_text_message(to_number, """
✉️ Por *mail*:

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
    send_text_message(to_number, "¡Si nos escribes, nos contactaremos contigo lo antes posible!")
    send_text_message(to_number, "🌐 Si quieres conocer más información, puedes visitar nuestra página web: https://tomasdevoto.edu.ar/")
    send_text_message(to_number, """
📱 Para estar al día con nuestras novedades, síguenos en nuestras redes sociales!:
*Instagram*:
https://www.instagram.com/institutotomasdevoto/
*YouTube*:
http://www.youtube.com/@itdstreaming
""")
    
    body_text = "En que otra cosa podemos ayudarte hoy?"
    
    opciones = opciones_menu_principal
    
    send_menu_list(to_number, body_text, opciones)

# --------------------------- Mensajes sobre inscripciones --------------------------- #










opciones_nivel_inicial_menu = [
        {"id": "menu_nivel_inicial_opt1", "title": "Propuestas pedagogicas 💡"},
        {"id": "menu_nivel_inicial_opt2", "title": "Horarios 🕒"},
        {"id": "menu_nivel_inicial_opt3", "title": "Talleres optativos 🎨"},
        {"id": "menu_nivel_inicial_opt4", "title": "Servicios adicionales 🧩"},
        {"id": "menu_nivel_inicial_opt5", "title": "Menu anterior 🔙"}
]

def nivel_inicial_message(to_number: str):
    send_text_message(to_number, "Buenisimo! 😄 Te contaré un poco sobre *Nivel Inicial*")
    send_text_message(to_number, "Promovemos aprender jugando en un entorno de afecto y confianza, donde se promueven valores como la empatía, la solidaridad y el respeto. Planificamos actividades lúdicas y significativas que fortalecen las capacidades cognitivas, sociales y expresivas de cada alumno. Integramos a las familias en la tarea educativa propiciando la comunicación, el diálogo constructivo y el respeto mutuo.")
    
    body_text = "En que lo podemos ayudar sobre *Nivel inicial*?"
    
    opciones = opciones_nivel_inicial_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_inicial_propuestas_pedagogicas(to_number: str):
    send_text_message(to_number, "💡 Algunas de nuestras propuestas *pedagogicas* en *Nivel inicial* son:")
    send_text_message(to_number, """
                        🇮🇹 *Italiano*:\nIniciamos a nuestros alumnos y alumnas en el conocimiento de la lengua italiana a partir de la sala de 3 años a través de propuestas lúdicas, literarias y musicales.\n\n🏐 *Educación fisica*:\nTrabajamos a partir de la sala de 2 años con propuestas de enseñanza para que el alumno/a explore, descubra y ponga en juego su motricidad.\n\n💻 *Educación digital*:\nIncluimos recursos digitales en el nivel inicial para que nuestros alumnos y alumnas desarrollen desde temprana edad habilidades que les permitirá seguir progresando en su trayectoria escolar.\n\n🎶 *Educación musical*:\nOfrecemos diferentes experiencias musicales para sensibilizar a los niños y a las niñas sobre el mundo sonoro con el fin de ampliar y enriquecer su repertorio cultural despertando el placer por la música y el goce por el hacer musical.
                    """)
    
    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel inicial*?"
    
    opciones = opciones_nivel_inicial_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_inicial_horarios(to_number: str):
    send_text_message(to_number, "🕜 Nuestros *horarios* en *Nivel inicial* son:")
    send_text_message(to_number, """
                        *TURNO MAÑANA*:\nSala de *2 años*/*3 años*   -   8:30 hs/12:15 hs\n\nSala de *4 años*/*5 años*   -   8:30 hs/12:30 hs\n\n*TURNO TARDE*:\nSala de *2 años*/*3 años*   -   13:20 hs/16:55 hs
                    """)
    send_text_message(to_number, "*Con jornada extendida optativa con comedor*")
    
    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel inicial*?"
    
    opciones = opciones_nivel_inicial_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_inicial_talleres_optativos(to_number: str):
    send_text_message(to_number, "🎨 Nuestros *Talleres optativos* en *Nivel inicial* son:")
    send_text_message(to_number, """
                        🎭 *Taller de artes visuales*:\nContribuir al conocimiento artístico a través del aporte de los diferentes recursos y técnicas, orientados a la generación de productos estéticos; dando un espacio al juego y a la creatividad desarrollando así modos de construcción personales de expresión y comunicación.\n\n🏃 *Taller de expresión y movimiento*:\nAcceder a prácticas corporales en el marco del lenguaje expresivo explorando a partir del movimiento diversos modos de conocer el mundo.\n\n⚾ *Taller de iniciación deportiva*:\nIntensificamos la práctica deportiva para que el niño/a logre un desarrollo integral a partir de diferentes experiencias corporales y motrices que continuarán en el Nivel Primario.\n\n🇬🇧 *Taller de inglés en convenio con la UTN – INSPT*:\nIniciamos a nuestros alumnos y alumnas en el conocimiento del inglés a través de propuestas lúdicas.\n\n🧩 *Taller de recreación*:\nLos niños y niñas participan de propuestas pedagógicas a través de situaciones lúdicas y recreativas.
                    """)

    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel inicial*?"
    
    opciones = opciones_nivel_inicial_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_inicial_servicios_adicionales(to_number:str):
    send_text_message(to_number, "🧩 Otros *servicios* de *Nivel inicial*:")
    send_text_message(to_number, """
                        🍴 *Comedor*:\nLos chicos y chicas cuentan con un comedor que les proporciona alimento nutritivo. \n\n🚌 *Transporte*:\nContamos con transporte, micros que los llevan a todos los lugares que sean necesarios.
                    """)
    
    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel inicial*?"
    
    opciones = opciones_nivel_inicial_menu
    
    send_menu_list(to_number, body_text, opciones)

##################################################################################################################################################################################

opciones_nivel_primario_menu = [
        {"id": "menu_nivel_primario_opt1", "title": "Propuestas pedagogicas 💡"},
        {"id": "menu_nivel_primario_opt2", "title": "Horarios 🕒"},
        {"id": "menu_nivel_primario_opt3", "title": "Algunos proyectos 📌"},
        {"id": "menu_nivel_primario_opt4", "title": "Talleres optativos 🎨"},
        {"id": "menu_nivel_primario_opt5", "title": "Servicios adicionales 🧩"},
        {"id": "menu_nivel_primario_opt6", "title": "Menu anterior 🔙"}
    ]

def nivel_primario_message(to_number: str):
    send_text_message(to_number, "Excelente! 😄 Te contaré un poco sobre *Nivel Primario*")
    send_text_message(to_number, "Nuestro propósito es que nuestros alumnos y alumnas crezcan y aprendan en un ambiente rico en experiencias que inviten a descubrir el mundo interactuando con otros en una saludable convivencia.")
    
    body_text = "En que lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_primario_propuestas_pedagogicas(to_number: str):
    send_text_message(to_number, "💡 Algunas de nuestras propuestas *pedagogicas* para *Nivel primario* son:")

    send_text_message(to_number, """
                        🏐 *Educacion Fisica*:
Trabajamos en dos jornadas obligatorias por la tarde los miércoles y viernes, asistiendo al campo de deportes del Club Ferrocarril Gral. Mitre. Jugar, poner el cuerpo en movimiento, aprender destrezas motoras y sobre todo participar de una tarde compartiendo deportes y recreación con compañeros y compañeras, son los objetivos del área de Educación Física. Ofrecemos una experiencia intensificada en horario que da identidad a nuestra escuela y que se mantiene durante los siete años del nivel.
""")

    send_text_message(to_number, """
                        🇮🇹 *Italiano*:
El italiano es el idioma que caracteriza  y da impronta identitaria a nuestra institución. Desde 1ro hasta 7mo grado, se van incrementando las horas de trabajo en el aula, que además de la enseñanza del idioma buscan acercar a los niños y niñas a la cultura, las tradiciones, los valores propios de Italia. Canciones, juegos, cuentos, poesías, novelas, materiales audiovisuales, son los estímulos a través de los cuales nuestros alumnos y alumnas se apropian gradualmente del idioma.

🇬🇧 *Ingles*:
El segundo idioma que ofrecemos dentro de nuestra propuesta educativa, es el inglés. Para un abordaje más intenso del área, la propuesta de la mañana puede complementarse con los talleres extracurriculares de inglés de turno tarde, dos veces a la semana y dos horas cada día.
""")
    
    send_text_message(to_number, """
                        🖌️ *Educacion Artistica*:\nBrindar a los/as alumnos/as la oportunidad de profundizar en los distintos lenguajes artísticos mediante experiencias estéticos-expresivas que le permitan conocerlos, disfrutarlos y comprenderlos.

🎵 *MÚSICA*: El aprendizaje de la música como una experiencia placentera en la cual el/la protagonista es el/la alumno/a y el continente es la música. La práctica y el hacer música es el rasgo de acción característico de todas las experiencias, sean estas para comprender las relaciones que se establecen en el discurso musical, para expresarse interpretándolo o para crear con los sonidos.

🎨 *PLÁSTICA*: Nuestro propósito es acrecentar el interés de los/as alumnos/as por el universo visual, ofreciendo propuestas de enseñanza progresivamente más complejas que les permitan ampliar sus conocimientos y su inserción en una cultura que, cómo la actual, ha potenciado la incidencia de lo visual en la vida cotidiana.

🎭 *TEATRO*:Los/as alumnos/as desarrollan la imaginación y la expresividad gestual, corporal y vocal dentro del juego organizado de la ficción. Se crean situaciones de enseñanza para que todos/as puedan utilizar el lenguaje teatral como medio de expresión y comunicación.
""")
    
    send_text_message(to_number, """
                        💻 *Educación tecnológica digital*:\nSe propone facilitar una vinculación comprensiva, coherente y crítica entre los alumnos/as y la técnica.

*TECNOLOGÍA*: Permite que los/as alumnos/as accedan a una comprensión de la tecnología que los habilite para interrogarse crítica, pero también creativamente, acerca de mundos pasados, presentes y futuros y del lugar que le cabe a todo ciudadano/a en la creación y el control de las tecnologías.

*INFORMÁTICA*: Se propone generar situaciones didácticas con empleo de variados materiales educativos informáticos en los cuales los/as alumnos/as se enfrentan a la necesidad de: 

- Seleccionar información, abordar distintas estrategias lectoras e interpretar múltiples situaciones escolares en las que se emplean variadas herramientas informáticas. 

- Promover situaciones que favorezcan conductas autónomas de los/as alumnos/as en el manejo de la computadora y la elaboración de sus trabajos, generando oportunidades para la adquisición de los conocimientos informáticos. 
""")

    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_primario_horarios(to_number: str):
    send_text_message(to_number, "🕜 Nuestros *horarios* en *Nivel primario* son:")
    
    send_text_message(to_number, """
                        *TURNO MAÑANA*:
*Ingreso*: 7:30hs - 7:40hs
de lunes a viernes (1ro a 7mo grado)

*Salida*: 12:30hs
de lunes a viernes (1ro a 2do grado)

*3ro a 7mo prolongación horaria de inglés hasta las 13:30hs*
(3er grado una vez a la semana, 4to a 7mo grado , dos veces por semana)            

""")

    send_text_message(to_number, """
                        *TURNO TARDE*:
*Lunes, martes y jueves de 14hs a 17hs:*
Talleres optativos extraprogramáticos.

*Miércoles y viernes de 14 a 17 horas:*
Taller de educación física en campo de deportes (modalidad obligatoria).

*3ro a 7mo prolongación horaria de inglés hasta las 13:30hs*
(3er grado una vez a la semana, 4to a 7mo grado , dos veces por semana)            
""")
    
    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_primario_algunos_proyectos(to_number: str):
    send_text_message(to_number, "📌 Algunos *proyectos* de *Nivel primario*:")
    send_text_message(to_number, """
                        🧑‍🤝‍🧑 *Proyecto padrinos y ahijados​*:
Proyecto que vincula a estudiantes de 7º grado con los niños y niñas de 1º grado, fomentando confianza y compañerismo. A lo largo del año comparten juegos, recreos, clases, desayunos y actividades especiales.

📖 *Animación a la lectura*:
Buscamos acercar a los niños y niñas a la lectura y a las prácticas de todo lector: disfrutar historias, buscar información, reflexionar y compartir emociones, participando activamente en la comunidad de lectores y escritores.

🌱 *Proyectos solidarios comunitarios*:
Promovemos la solidaridad como actitud de vida, aprendida y puesta en práctica con compromiso afectivo. Colaboramos con la escuela N°442 Agua Amarilla y realizamos campañas solidarias, siempre abiertos a nuevas experiencias comunitarias.

🧠 *Proyecto ESI (Educación Sexual Integral)*:
La ESI, según la ley 26.150, se integra en todas las áreas curriculares para desarrollar empatía, expresión de emociones y respeto. La participación familiar es clave para garantizar el derecho de los niños y niñas a informarse, preguntar y expresarse en una sociedad plural y respetuosa.

🏆 *Juegos Interbandos*:
Durante el año, los bandos blanco, rojo y verde participan en juegos y desafíos para sumar puntos. En el encuentro final, las familias se suman para alentar y se anuncia el equipo ganador, celebrando esfuerzo, compañerismo y actitud deportiva.

⛺ *Campamentos*:
Desde hace años realizamos campamentos y actividades en la naturaleza, donde los chicos aprenden a cuidar el medio ambiente, disfrutar del cielo estrellado, compartir canciones, jugar y convivir con animales y plantas. Cada grado tiene su destino: 1º-3º Ezeiza o Villa Adelina, 4º Rosario, 5º Tandil, 6º Entre Ríos y 7º Córdoba.
""")

    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_primario_talleres_optativos(to_number: str):
    send_text_message(to_number, "🎨 Algunos *talleres optativos* de *Nivel primario*:")
    send_text_message(to_number, """
                        🖌️ *Taller de Arte​*:
El taller de Arte es un espacio para el goce estético de la creación, brindando al niño un ambiente de estímulos que despierten su creatividad, su capacidad perceptiva, sensitiva y expresiva. El taller estimula la autogestión y la autonomía enriqueciendo la influencia del arte que llega a la mente y a la emoción potenciando el desarrollo de una personalidad integral.

🥋 *Taller de Taekwondo*:
Es uno de los talleres que se dictan por la tarde. Taekwondo conduce a los niños a desarrollar conductas no violentas, les enseña la disciplina, les fomenta el autocontrol y los ayuda a valorar la importancia del respeto mutuo.

🌱 *Taller de ingles - UTN*:
Promovemos la solidaridad como actitud de vida, aprendida y puesta en práctica con compromiso afectivo. Colaboramos con la escuela N°442 Agua Amarilla y realizamos campañas solidarias, siempre abiertos a nuevas experiencias comunitarias.
""")

    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

def nivel_primario_servicios_adicionales(to_number:str):
    send_text_message(to_number, "🧩 Otros *servicios* de *Nivel primario*:")
    send_text_message(to_number, """
                        🍴 *Comedor*:\nLos chicos y chicas cuentan con un comedor que les proporciona alimento nutritivo. \n\n🚌 *Transporte*:\nContamos con transporte, micros que los llevan a todos los lugares que sean necesarios.
                    """)
    
    body_text = "En que otra cosa lo podemos ayudar sobre *Nivel primario*?"
    
    opciones = opciones_nivel_primario_menu
    
    send_menu_list(to_number, body_text, opciones)

