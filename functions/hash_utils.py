# functions/hash_utils.py
import os
import hmac
import hashlib

def get_identifier_hash(phone_number: str) -> str:
    """
    Devuelve un HMAC-SHA256 hex digest usando la clave secreta HASH_KEY.
    """
    key = os.getenv("HASH_KEY")
    if not key:
        raise RuntimeError("HASH_KEY no encontrada en variables de entorno")

    key_bytes = key.encode()
    msg = phone_number.encode()
    h = hmac.new(key_bytes, msg, hashlib.sha256)
    return h.hexdigest()
