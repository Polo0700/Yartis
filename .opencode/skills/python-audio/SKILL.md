---
name: python-audio
description: |
  Python audio processing for Yartis voice assistant: recording with pyaudio,
  noise reduction with noisereduce (spectral gating), VAD with webrtcvad,
  FFT analysis with numpy/scipy, audio format conversion, and chunked
  streaming. Use when working with microphone input, WAV files, PCM buffers,
  sample rate conversion, or any audio signal processing in Python.
  Triggers: audio, pyaudio, noisereduce, webrtcvad, VAD, FFT, numpy, scipy,
  microphone, recording, WAV, PCM, sample rate, chunk, streaming.
---

# Python Audio Processing — Yartis

## Stack
- `pyaudio` — captura de micrófono (PortAudio binding)
- `noisereduce` — spectral gating noise reduction
- `webrtcvad` — voice activity detection (WebRTC)
- `numpy` — buffers, FFT, slicing
- `scipy.signal` — resample, filtros, spectrogram
- `soundfile` / `scipy.io.wavfile` — lectura/escritura WAV
- `struct` — parsing PCM raw bytes

## Recording básico

```python
import pyaudio
import numpy as np

CHUNK = 1600       # 100ms @ 16kHz
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
for _ in range(0, int(RATE / CHUNK * 5)):  # 5 segundos
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

audio_bytes = b''.join(frames)
audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
```

## Recording con VAD (detección de silencio)

```python
import pyaudio
import webrtcvad

vad = webrtcvad.Vad(2)  # agresividad: 0 (mínima) a 3 (máxima)

def record_until_silence(silence_secs: float = 1.5) -> bytes:
    CHUNK = 1600  # 100ms @ 16kHz -> 1600 frames == 100ms
    SILENCE_CHUNKS = int(silence_secs * RATE / CHUNK)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    frames: list[bytes] = []
    silence_count = 0
    speech_detected = False

    while silence_count < SILENCE_CHUNKS:
        data = stream.read(CHUNK)
        frames.append(data)

        is_speech = vad.is_speech(data, RATE)
        if is_speech:
            speech_detected = True
            silence_count = 0
        elif speech_detected:
            silence_count += 1

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)
```

## Noise reduction

```python
import noisereduce as nr
import numpy as np

def clean_audio(audio: np.ndarray, rate: int, noise_profile: np.ndarray | None = None) -> np.ndarray:
    """
    Reduce noise via spectral gating.
    Si no se pasa noise_profile, toma los primeros 500ms como perfil de ruido.
    """
    return nr.reduce_noise(
        y=audio,
        sr=rate,
        y_noise=noise_profile,        # None = auto desde primeros frames
        prop_decrease=0.8,            # 0.0 = nada, 1.0 = máximo
        n_fft=512,                    # tamaño ventana FFT
        win_length=None,
        hop_length=128,
        stationary=False,             # True si el ruido es constante
        time_constant_s=2.0,
    )
```

## FFT analysis

```python
import numpy as np
from scipy.fft import rfft, rfftfreq

def get_spectrum(audio: np.ndarray, rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Retorna frecuencias y magnitud del espectro"""
    n = len(audio)
    freqs = rfftfreq(n, d=1/rate)
    magnitudes = np.abs(rfft(audio))
    return freqs, magnitudes

def get_energy(audio: np.ndarray) -> float:
    """RMS energy del frame"""
    return np.sqrt(np.mean(audio**2))
```

## Buffer circular para audio

```python
import numpy as np
from collections import deque

class AudioBuffer:
    """Buffer circular para audio streaming"""
    def __init__(self, max_seconds: float = 3.0, rate: int = 16000):
        self.max_samples = int(max_seconds * rate)
        self.buffer = deque(maxlen=self.max_samples)
        self.rate = rate

    def push(self, samples: np.ndarray) -> None:
        self.buffer.extend(samples.tolist())

    def get(self) -> np.ndarray:
        return np.array(self.buffer, dtype=np.float32)

    def clear(self) -> None:
        self.buffer.clear()
```

## Sample rate conversion

```python
from scipy import signal

def resample(audio: np.ndarray, orig_rate: int, target_rate: int = 16000) -> np.ndarray:
    """Re-muestrea audio a target_rate usando FIR filtering"""
    number_of_samples = int(len(audio) * target_rate / orig_rate)
    return signal.resample(audio, number_of_samples)
```

## Guardar/Leer WAV

```python
import soundfile as sf
import numpy as np

def save_wav(path: str, audio: np.ndarray, rate: int = 16000) -> None:
    sf.write(path, audio, rate)

def load_wav(path: str) -> tuple[np.ndarray, int]:
    return sf.read(path, dtype=np.float32)
```

## Pipeline de audio completo

```python
def process_audio_bytes(audio_bytes: bytes) -> np.ndarray:
    """Pipeline: bytes PCM → float32 → noise reduction"""
    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    audio = clean_audio(audio, RATE)
    return audio
```

## Consideraciones de performance

- **Chunks de 100ms** (1600 samples @ 16kHz) — balance entre latency y overhead
- **Float32** en lugar de int16 para procesamiento (Whisper espera float32)
- **Noisereduce** puede ser lento en CPU para audios largos — considerar procesar en chunks
- **VAD** opera sobre bytes raw, no float32 (es más rápido)
