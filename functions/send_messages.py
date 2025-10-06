import os
import requests
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

test = False

def send_menu_list(to_number: str, text: str, options: list):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": text},
            "footer": {"text": "Eliga una opcion del menu"},
            "action": {
                "button": "Menu",
                "sections": [
                    {
                        "title": "Opciones principales",
                        "rows": options
                    }
                ]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_text_message(to_number: str, message: str):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_img_message(to_number: str, media_id: str, caption: str = ""):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "image",
        "image": {
            "id": media_id,
            "caption": caption
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_sticker_message(to_number: str, media_id: str):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "sticker",
        "sticker": {
            "id": media_id
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_pdf_message(to_number: str, media_id: str, filename: str):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": filename
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_link_message(to_number: str, link_url: str, link_title: str):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }

    # Texto con solo título y link en el cuerpo
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": f"{link_title}\n{link_url}"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass

def send_contact_message(to_number: str, contact_name: str, contact_phone: str):
    url = f"https://graph.facebook.com/{os.getenv('META_API_VERSION')}/{os.getenv('META_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('META_TOKEN')}",
        "Content-Type": "application/json"
    }
    vcard = (
        f"BEGIN:VCARD\n"
        f"VERSION:3.0\n"
        f"N:{contact_name};;;;\n"
        f"FN:{contact_name}\n"
        f"TEL;TYPE=CELL:{contact_phone}\n"
        f"END:VCARD"
    )
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "contacts",
        "contacts": [
            {
                "addresses": [],
                "birthday": None,
                "emails": [],
                "name": {
                    "formatted_name": contact_name,
                    "first_name": contact_name,
                    "last_name": ""
                },
                "org": None,
                "phones": [
                    {
                        "phone": contact_phone,
                        "type": "CELL"
                    }
                ],
                "urls": []
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if test:
        if response.status_code == 200:
            print(Fore.GREEN + f"✓ Menú con botones enviado a {to_number}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Error al enviar menú ({response.status_code}): {response.text}" + Style.RESET_ALL)
    else:
        pass