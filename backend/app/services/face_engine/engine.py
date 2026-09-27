"""Motor facial de la Fase A [Añadido, fuera del documento]: detección (YuNet) + embedding
(SFace) + comparación. La comparación reutiliza `algorithms.vector_ops.dot_product` — la
misma operación de álgebra lineal de la Fase 4 (PDF §11), aplicada al mismo problema: decidir
si dos vectores (aquí, dos rostros) son "el mismo".
"""

from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np

from app.algorithms import vector_ops

MODELS_DIR = Path(__file__).resolve().parents[3] / "models"
DETECTOR_PATH = MODELS_DIR / "face_detection_yunet_2023mar.onnx"
RECOGNIZER_PATH = MODELS_DIR / "face_recognition_sface_2021dec.onnx"

# Nombre del modelo guardado junto a cada vector: si algún día cambia el motor, un vector de
# SFace nunca se compara contra uno de otro modelo (mismo criterio que Aurora, D107).
MODELO_NOMBRE = "sface-2021dec"

# Umbral recomendado por OpenCV para SFace con similitud coseno. Provisional, sin calibrar
# con fotos reales del equipo (misma advertencia que Aurora hizo con el suyo, D106).
UMBRAL_SIMILITUD = 0.363


class RostroRechazado(Exception):
    """La imagen no tiene exactamente un rostro utilizable."""


@lru_cache
def _detector() -> cv2.FaceDetectorYN:
    return cv2.FaceDetectorYN.create(str(DETECTOR_PATH), "", (320, 320), score_threshold=0.6)


@lru_cache
def _recognizer() -> cv2.FaceRecognizerSF:
    return cv2.FaceRecognizerSF.create(str(RECOGNIZER_PATH), "")


def modelos_disponibles() -> bool:
    """False si a este entorno le faltan los pesos (no se descargan solos, hay que bajarlos
    a mano en `backend/models/`, igual que en Aurora)."""
    return DETECTOR_PATH.exists() and RECOGNIZER_PATH.exists()


def calcular_embedding(imagen_bytes: bytes) -> np.ndarray:
    """Decodifica la imagen, exige exactamente un rostro, y devuelve su vector (128 floats).
    La imagen decodificada se descarta apenas termina esta función: nunca se guarda."""
    datos = np.frombuffer(imagen_bytes, dtype=np.uint8)
    imagen = cv2.imdecode(datos, cv2.IMREAD_COLOR)
    if imagen is None:
        raise RostroRechazado("No se pudo leer la imagen.")

    detector = _detector()
    alto, ancho = imagen.shape[:2]
    detector.setInputSize((ancho, alto))
    _, rostros = detector.detect(imagen)

    if rostros is None or len(rostros) == 0:
        raise RostroRechazado("No se detectó un rostro.")
    if len(rostros) > 1:
        raise RostroRechazado(
            f"Se detectaron {len(rostros)} rostros. Envía una foto con una sola persona."
        )

    recognizer = _recognizer()
    alineado = recognizer.alignCrop(imagen, rostros[0])
    embedding = recognizer.feature(alineado)
    return embedding.flatten().astype(np.float32)


def similitud_coseno(a: np.ndarray, b: np.ndarray) -> float:
    """cos(A, B) = (A·B) / (‖A‖·‖B‖) — el producto escalar es el mismo `dot_product()` de la
    Fase 4 [PDF §11.1]."""
    producto = vector_ops.dot_product(a.tolist(), b.tolist())
    norma_a = float(np.linalg.norm(a))
    norma_b = float(np.linalg.norm(b))
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return producto / (norma_a * norma_b)


def a_bytes(embedding: np.ndarray) -> bytes:
    return embedding.astype(np.float32).tobytes()


def desde_bytes(data: bytes) -> np.ndarray:
    return np.frombuffer(data, dtype=np.float32)
