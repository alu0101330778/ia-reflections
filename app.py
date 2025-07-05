from sentence_transformers import SentenceTransformer
import numpy as np
import json
import unicodedata

def normalize_emotion(emotion: str) -> str:
    return unicodedata.normalize("NFKD", emotion.lower()).encode("ASCII", "ignore").decode("utf-8")

model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

with open("reflections.json", "r", encoding="utf-8") as f:
    reflections = json.load(f)

# Crear textos de entrada solo con emociones normalizadas
texts = [
    " ".join([normalize_emotion(e) for e in r.get("tags", [])])
    for r in reflections
]

# Mostrar los 10 primeros textos para verificar

embeddings = model.encode(texts)

np.save("embeddings.npy", embeddings)

# Guardar también los textos originales (reflections.json no modificado)
with open("reflections_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(reflections, f, ensure_ascii=False, indent=2)
