import requests
import threading
import json

WEBHOOK_URL = "http://127.0.0.1:5000/webhook"  # tu webhook local

def enviar_mensaje(i):
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {"id": f"msg-{i}", "type": "text", "text": {"body": f"Mensaje de prueba {i}"}}
                            ],
                            "contacts": [
                                {"profile": {"name": f"Usuario {i}"}, "wa_id": f"54911111111{i:02d}"}
                            ]
                        }
                    }
                ]
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"✅ Mensaje {i} enviado")
    except Exception as e:
        print(f"❌ Error mensaje {i}: {e}")

threads = []
for i in range(50):  # 50 mensajes simultáneos
    t = threading.Thread(target=enviar_mensaje, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ Test finalizado")
