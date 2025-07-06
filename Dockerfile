# Etapa de build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

# Instala las dependencias sin caché
RUN pip install --no-cache-dir -r requirements.txt

# Etapa de ejecución
FROM python:3.11-slim

WORKDIR /app

# Copia solo lo necesario desde la build anterior
COPY --from=builder /usr/local /usr/local

# Copia tu código fuente
COPY . .

# Expone el puerto Flask
EXPOSE 5000

# Comando de arranque (ajustar si usas otro archivo)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]
