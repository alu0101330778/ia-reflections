# ia-reflections

Este proyecto utiliza modelos de lenguaje para analizar y comparar reflexiones emocionales mediante embeddings y similitud de coseno.

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

3. Crea un archivo `.env` con la variable `API_SECRET_KEY`:

   ```
   API_SECRET_KEY=tu_clave_secreta
   ```

## Uso

### 1. Preparar los datos

Ejecuta el script [`app.py`](ia-reflections/app.py) para generar los embeddings y limpiar los datos:

```sh
python app.py
```

Esto creará los archivos `embeddings.npy` y `reflections_cleaned.json` a partir de `reflections.json`.

### 2. Iniciar la API

Lanza el servidor Flask ejecutando [`api.py`](ia-reflections/api.py):

```sh
python api.py
```

La API estará disponible en `http://localhost:5000/ia/reflection`.

### 3. Realizar peticiones

Envía una petición POST a `/ia/reflection` con el texto y la cabecera `X-Signature` (firma HMAC SHA256 del cuerpo usando tu clave secreta).

## ¿Cómo funciona?

- [`app.py`](ia-reflections/app.py) normaliza las emociones de las reflexiones y genera embeddings usando el modelo `distiluse-base-multilingual-cased-v1`.
- Los embeddings y los datos limpios se guardan para su uso posterior.
- [`api.py`](ia-reflections/api.py) expone una API REST que recibe un texto, calcula su embedding y busca la reflexión más similar usando la similitud de coseno.
- La autenticación se realiza mediante una firma HMAC en la cabecera `X-Signature`.