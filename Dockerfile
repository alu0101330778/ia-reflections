FROM python:3.11-slim

WORKDIR /app

# Copiar solo archivos necesarios
COPY api.py reflections_encrypted.bin embeddings.npy ./
COPY requirements.txt .env ./

# Instalar dependencias (incluye torch CPU-only)
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]
