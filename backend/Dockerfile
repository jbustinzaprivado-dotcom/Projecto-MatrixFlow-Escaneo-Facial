# [Añadido en el repaso de fidelidad §16-21, PDF §17] Imagen del backend para docker-compose.
FROM python:3.11-slim

# libgl1/libglib2.0-0: opencv-python-headless los necesita en tiempo de ejecución aunque no
# use ventanas — sin ellos, `import cv2` falla en una imagen Debian mínima.
# curl: para descargar los pesos ONNX en el paso siguiente.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Los pesos ONNX (backend/models/*.onnx) están ignorados por git a propósito (D45, ~39 MB).
# En desarrollo local se descargan a mano (ver README.md); para que un build remoto sin
# acceso a ese disco (Render, o cualquier CI) funcione igual, se descargan aquí desde el
# repositorio oficial de OpenCV si todavía no existen — `media.githubusercontent.com`, no
# `raw.githubusercontent.com`, porque ese repo los versiona con Git LFS (raw solo da el
# puntero de texto, no el binario).
RUN mkdir -p models && \
    [ -f models/face_detection_yunet_2023mar.onnx ] || \
    curl -fsSL -o models/face_detection_yunet_2023mar.onnx \
      https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx && \
    [ -f models/face_recognition_sface_2021dec.onnx ] || \
    curl -fsSL -o models/face_recognition_sface_2021dec.onnx \
      https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx

EXPOSE 8000

# [Añadido, corrige hallazgo del análisis de código] `--proxy-headers --forwarded-allow-ips='*'`:
# en Render (y en este mismo docker-compose), el único que puede conectarse directo al
# contenedor es el balanceador/proxy — así que confiar en el `X-Forwarded-For` que agrega es
# seguro. Sin esto, `request.client.host` (usado por el limitador de /verificacion, el único
# endpoint sin sesión del backend) ve siempre la IP interna del proxy, no la del usuario real:
# el límite "10 intentos por minuto por IP" se vuelve un solo cupo compartido por todos.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'"]
