from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import hmac
import hashlib
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Cargar variables de entorno
load_dotenv()
SECRET_KEY = os.getenv("API_SECRET_KEY")
REFLECTIONS_KEY = os.getenv("REFLECTIONS_SECRET_KEY")
fernet = Fernet(REFLECTIONS_KEY.encode())

app = Flask(__name__)

def verify_signature(req):
    received_sig = req.headers.get("X-Signature")
    body = req.get_data()  # cuerpo crudo (bytes)

    expected_sig = hmac.new(
        SECRET_KEY.encode(), body, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(received_sig, expected_sig)


def normalize_emotion(emotion: str) -> str:
    return unicodedata.normalize("NFKD", emotion.lower()).encode("ASCII", "ignore").decode("utf-8")

# Cargar modelo y datos
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

with open("reflections_encrypted.bin", "rb") as f:
    encrypted_data = f.read()

decrypted_data = fernet.decrypt(encrypted_data)
reflections = json.loads(decrypted_data)

embeddings = np.load("embeddings.npy")

@app.route("/ia/reflection", methods=["POST"])
def get_reflection():
    if not verify_signature(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    emotions = data.get("emotions", [])
    if not emotions:
        return jsonify({"error": "No emotions provided"}), 400

    # Normalizar emociones recibidas
    normalized_emotions = [normalize_emotion(e) for e in emotions]
    query = " ".join(normalized_emotions)

    query_embedding = model.encode([query])

    # Calcular puntuaciones
    scored = []

    for i, r in enumerate(reflections):
        normalized_tags = [normalize_emotion(tag) for tag in r.get("tags", [])]
        common_emotions = set(normalized_emotions) & set(normalized_tags)

        if not common_emotions:
            continue  # ignorar si no hay ninguna coincidencia

        emotion_match_score = len(common_emotions) / len(normalized_emotions)  # de 0 a 1
        similarity = cosine_similarity(query_embedding, [embeddings[i]])[0][0]

        combined_score = (similarity * 0.7) + (emotion_match_score * 0.3)  # pesos ajustables
        scored.append((combined_score, r))

    if not scored:
        return jsonify({"error": "No reflections matched any of the given emotions"}), 404

    # Ordenar por puntuación combinada descendente
    scored.sort(key=lambda x: x[0], reverse=True)

    # Selección aleatoria entre el top-N
    N = 10
    top_reflections = [r for _, r in scored[:N]]
    selected_reflection = np.random.choice(top_reflections)

    return jsonify({
        "reflection": {
            "title": selected_reflection["title"],
            "body": selected_reflection["body"],
            "end": selected_reflection["end"],
            "tags": selected_reflection["tags"]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
