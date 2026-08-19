---
name: python-whisper
description: |
  faster-whisper integration for Yartis: speech-to-text with GPU acceleration,
  model selection (tiny/small/medium/large), language detection, VAD filter,
  word-level timestamps, and transcription pipeline optimization.
  Use when transcribing audio, selecting Whisper models, optimizing GPU
  inference, or handling transcription errors.
  Triggers: Whisper, faster-whisper, STT, speech-to-text, transcription,
  GPU, CUDA, transformer, CTranslate2, language detection.
---

# faster-whisper — Yartis STT

## Stack
- `faster-whisper` — wrapper sobre CTranslate2 para Whisper
- `ctranslate2` — backend de inferencia (GPU/CPU)
- `nvidia-cublas` / `nvidia-cudnn` — aceleración GPU

## Modelos disponibles

| Modelo | Parámetros | RAM | GPU VRAM | Velocidad | Precisión |
|--------|-----------|-----|----------|-----------|-----------|
| `tiny` | 39M | ~1GB | ~1GB |  |  |
| `base` | 74M | ~1GB | ~1GB |  |  |
| `small` | 244M | ~2GB | ~2GB |  |  |
| `medium` | 769M | ~5GB | ~5GB |  |  |
| `large-v3` | 1550M | ~10GB | ~10GB |  |  |

**Recomendación Yartis:** `small` (balance velocidad/precisión, funciona en GPUs de 4GB+).

## Uso básico

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cuda", compute_type="float16")

segments, info = model.transcribe("audio.wav", language="es")

print(f"Idioma: {info.language} (prob: {info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## Transcribir desde numpy array

```python
import numpy as np

def transcribe_array(model: WhisperModel, audio: np.ndarray) -> str:
    """Transcribe un numpy array float32 directamente"""
    segments, _ = model.transcribe(audio, language="es")
    return " ".join(seg.text for seg in segments)
```

## Transcribir con timestamps palabra por palabra

```python
segments, _ = model.transcribe(
    "audio.wav",
    language="es",
    word_timestamps=True  # activa timestamps por palabra
)

for segment in segments:
    for word in segment.words:
        print(f"  {word.word} [{word.start:.2f} - {word.end:.2f}] (prob: {word.probability:.2f})")
```

## VAD filter (saltar silencios)

```python
segments, _ = model.transcribe(
    "audio.wav",
    language="es",
    vad_filter=True,              # activa VAD interno
    vad_parameters=dict(
        threshold=0.5,            # sensibilidad (0-1)
        min_speech_duration_ms=250,
        min_silence_duration_ms=100,
    )
)
```

## Configuración optimizada para GPU

```python
model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16",         # float16 es 2x más rápido que float32
    cpu_threads=4,                  # threads para CPU (si cae a CPU)
    num_workers=1,                  # workers para batch
    local_files_only=False,         # descargar si no está en cache
)
```

## Pipeline completo Yartis

```python
import numpy as np
from faster_whisper import WhisperModel
from core.audio import process_audio_bytes  # noise reduction

class Transcriber:
    def __init__(self, model_name: str = "small"):
        self.model = WhisperModel(
            model_name,
            device="cuda",
            compute_type="float16"
        )

    def transcribe(self, audio_bytes: bytes) -> str:
        # 1. Limpiar audio
        audio = process_audio_bytes(audio_bytes)

        # 2. Transcribir
        segments, info = self.model.transcribe(
            audio,
            language="es",
            vad_filter=True,
        )

        # 3. Unir segmentos
        return " ".join(seg.text.strip() for seg in segments)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `CUDA out of memory` | Modelo muy grande para la GPU | Usar `small` en vez de `large`, o `compute_type="int8_float16"` |
| `RuntimeError: model not found` | No se descargó el modelo | `local_files_only=False` en la primera vez |
| `No module named 'ctranslate2'` | Falta dependencia | `uv add faster-whisper ctranslate2` |
| Transcripción en inglés | `language` no especificado | Pasar `language="es"` |
| Segmentos vacíos | Audio muy ruidoso | Aplicar noise reduction antes |
| Latencia alta | compute_type="float32" | Cambiar a `float16` |
