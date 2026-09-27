# [Añadido en el repaso de fidelidad §16-21, PDF §17] Imagen del backend para docker-compose.
FROM python:3.11-slim

# libgl1/libglib2.0-0: opencv-python-headless los necesita en tiempo de ejecución aunque no
# use ventanas — sin ellos, `import cv2` falla en una imagen Debian mínima.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Los pesos ONNX (backend/models/*.onnx) están ignorados por git (D45): esta imagen solo
# funciona de verdad si ya existen en el disco donde se hace `docker build` — descárgalos
# primero (ver README.md) o el motor facial responderá 503 (`modelos_disponibles()` en falso).

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
