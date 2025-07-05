# ia-reflections

Este proyecto utiliza modelos de lenguaje para analizar y comparar reflexiones emocionales mediante embeddings y similitud de coseno. Incluye un sistema de encriptación para proteger las reflexiones almacenadas.

## Instalación

1. Clona este repositorio y accede a la carpeta `ia-reflections`:

   ```sh
   git clone <URL-del-repositorio>
   cd ia-reflections
   ```

2. Instala las dependencias necesarias:

   ```sh
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` con las siguientes variables:

   ```
   API_SECRET_KEY=tu_clave_secreta
   REFLECTIONS_SECRET_KEY=tu_clave_fernet_generada
   ```

   - Puedes generar una clave Fernet ejecutando en Python:
     ```python
     from cryptography.fernet import Fernet
     print(Fernet.generate_key().decode())
     ```

## Uso

### 1. Preparar los datos

Ejecuta el script [`app.py`](ia-reflections/app.py) para generar los embeddings y limpiar los datos:

```sh
python app.py
```

Esto creará los archivos `embeddings.npy` y `reflections_cleaned.json` a partir de `reflections.json`.

### 2. Encriptar las reflexiones

Para proteger las reflexiones, ejecuta el script [`reflections_encrypter.py`](ia-reflections/reflections_encrypter.py):

```sh
python reflections_encrypter.py
```

Esto encriptará el archivo `reflections_cleaned.json` y generará `reflections_encrypted.bin`, que será utilizado por la API.

### 3. Iniciar la API

Lanza el servidor Flask ejecutando [`api.py`](ia-reflections/api.py):

```sh
python api.py
```

La API estará disponible en `http://localhost:5000/ia/reflection`.

### 4. Realizar peticiones

Envía una petición POST a `/ia/reflection` con el texto y la cabecera `X-Signature` (firma HMAC SHA256 del cuerpo usando tu clave secreta).

## ¿Cómo funciona?

- [`app.py`](ia-reflections/app.py) normaliza las emociones de las reflexiones y genera embeddings usando el modelo `distiluse-base-multilingual-cased-v1`.
- Los embeddings y los datos limpios se guardan para su uso posterior.
- [`reflections_encrypter.py`](ia-reflections/reflections_encrypter.py) encripta las reflexiones limpias usando una clave Fernet definida en el `.env`.
- [`api.py`](ia-reflections/api.py) expone una API REST que recibe un texto, calcula su embedding y busca la reflexión más similar usando la similitud de coseno. Desencripta las reflexiones en tiempo de ejecución usando la clave Fernet.
- La autenticación se realiza mediante una firma HMAC en la cabecera `X-Signature`.