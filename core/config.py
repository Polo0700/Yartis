from pathlib import Path

RATE = 16000
CHUNK = 1024
CHANNELS = 1
DTYPE = "int16"

WHISPER_MODEL = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE = "int8"
WHISPER_BEAM = 5

UMBRAL_SILENCIO = 50
PASOS_SILENCIO_LIMITE = 35
SEGUNDOS_POST_SILENCIO = 5

# OpenWakeWord
WAKE_WORD = "yartis"  # nombre del modelo de wake word
WAKE_FRAME = 1280  # samples por frame (OpenWakeWord requiere 1280)
WAKE_THRESHOLD = 0.3  # sensibilidad (0-1, más alto = menos falsos positivos)
WAKE_MODEL_PATH = str(Path(__file__).parent / "models" / "yartis.onnx")

DEBUG = True  # True = muestra scores de audio (para verificar señal)

# Candidatos para wake word personalizada:
# - Kalt (alemán, una sílaba, K+L+T)
# - Takto (inventada, T+K+T)
# - Xetra (inventada, ks+t+r)
# - Yatis (inventada, Y+T+S)
