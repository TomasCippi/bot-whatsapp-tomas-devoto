import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# =================================================================
# ⚙️ CONFIGURACIÓN DE LA PRUEBA
# =================================================================

# URL donde está corriendo tu bot (reemplaza con la IP o dominio de tu VPS)
# Si está en tu máquina local, usa http://127.0.0.1:5000
URL_WEBHOOK = "https://21389366b452.ngrok-free.app/webhook"

# Número de peticiones (mensajes) a enviar.
# ⚠️ ADVERTENCIA: No excedas los 500 o puedes recibir penalizaciones de Meta.
NUM_MENSAJES = 100 

# Concurrencia: Cuántos mensajes enviar a la vez (simula hilos de usuarios)
# Prueba con 20, 50, y luego sube a 100 o más.
HILOS_CONCURRENTES = 20 

# Número que tu bot está usando en modo hardcodeo (debe coincidir con main.py)
NUMERO_TEST = "5491158633746" 
NOMBRE_TEST = "UsuarioStressTest"

# =================================================================
# 📥 PAYLOAD (Cuerpo del Mensaje de WhatsApp)
# =================================================================
def crear_payload(num_msg):
    """Crea un payload de WhatsApp simulando un mensaje de texto."""
    
    # Aquí puedes cambiar el texto, por ejemplo, para simular clics en opciones
    texto_a_enviar = f"Hola, prueba de carga N° {num_msg}"
    
    return {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    # IMPORTANTE: Cambiamos el 'from' para simular usuarios distintos
                                    # si deseas probar la inserción en DB. Si no, usa el NUMERO_TEST.
                                    "from": NUMERO_TEST, 
                                    "id": f"wamid.TEST_{num_msg}",
                                    "type": "text",
                                    "text": {"body": texto_a_enviar}
                                }
                            ],
                            "contacts": [
                                {"profile": {"name": NOMBRE_TEST}}
                            ]
                        }
                    }
                ]
            }
        ]
    }

# =================================================================
# 💻 FUNCIÓN DE ENVÍO Y MONITOREO
# =================================================================
def enviar_mensaje(num_msg):
    payload = crear_payload(num_msg)
    
    # Medir el tiempo de respuesta del webhook
    inicio = time.time()
    
    try:
        # Enviamos la petición POST
        response = requests.post(URL_WEBHOOK, json=payload, timeout=5) 
        fin = time.time()
        
        tiempo_respuesta = round((fin - inicio) * 1000, 2) # en milisegundos

        if response.status_code == 200:
            print(f"✅ Mensaje {num_msg} enviado. Webhook respondió en {tiempo_respuesta} ms.")
        else:
            print(f"❌ Mensaje {num_msg} ERROR. Código: {response.status_code}. Tiempo: {tiempo_respuesta} ms.")
    
    except requests.exceptions.Timeout:
        # Esto es un error CRÍTICO, significa que tu bot no respondió a Meta a tiempo.
        print(f"🔴 Mensaje {num_msg} FALLÓ. El Webhook excedió el tiempo límite (5s).")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Mensaje {num_msg} FALLÓ CONEXIÓN: {e}")

# =================================================================
# 🏁 EJECUCIÓN PRINCIPAL
# =================================================================
if __name__ == "__main__":
    print(f"\n--- INICIANDO PRUEBA DE CARGA ---")
    print(f"Peticiones a enviar: {NUM_MENSAJES}")
    print(f"Hilos concurrentes: {HILOS_CONCURRENTES}")
    print(f"URL: {URL_WEBHOOK}\n")
    
    start_time = time.time()
    
    # Usamos ThreadPoolExecutor para enviar peticiones en paralelo
    with ThreadPoolExecutor(max_workers=HILOS_CONCURRENTES) as executor:
        # Generamos una lista de tareas (mensajes 1 a NUM_MENSAJES)
        executor.map(enviar_mensaje, range(1, NUM_MENSAJES + 1))
        
    end_time = time.time()
    
    duracion_total = round(end_time - start_time, 2)
    print(f"\n--- PRUEBA FINALIZADA ---")
    print(f"Duración total: {duracion_total} segundos.")
    print(f"Peticiones por segundo: {round(NUM_MENSAJES / duracion_total, 2)}")