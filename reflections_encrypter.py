from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json

# Cargar variables de entorno
load_dotenv()
key = os.getenv("REFLECTIONS_ENCRYPTION_KEY")

if not key:
    raise ValueError("La clave REFLECTIONS_ENCRYPTION_KEY no está definida en el .env")

try:
    fernet = Fernet(key.encode())
except Exception as e:
    raise ValueError("La clave no es válida para Fernet. Asegúrate de haberla generado con Fernet.generate_key().") from e

# Cargar reflexiones
with open("reflections_cleaned.json", "r", encoding="utf-8") as f:
    data = f.read()

# Encriptar
encrypted = fernet.encrypt(data.encode("utf-8"))

# Guardar archivo encriptado
with open("reflections_encrypted.bin", "wb") as f:
    f.write(encrypted)

print("Reflexiones encriptadas y guardadas en reflections_encrypted.bin")
