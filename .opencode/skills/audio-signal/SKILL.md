---
name: audio-signal
description: |
  Audio processing and signal concepts for the Yartis voice assistant.
  Use when working with audio recording, FFT, noise reduction, wake word
  detection, VAD (voice activity detection), sample rates, and audio
  formats (WAV, PCM) in both Python and Rust.
  Triggers: audio, FFT, noise reduction, recording, VAD, sample rate, WAV, PCM,
  microphone, speech, whisper, wake word.
---

# Audio & Signal Processing — Yartis

## Pipeline de audio

```
Micrófono → buffer PCM → noise reduction (spectral gating) → VAD → Whisper
```

## Conceptos clave

### Sample Rate
- **16 kHz** (16000) — estándar para Whisper y reconocimiento de voz
- **44.1 kHz** — CD quality, innecesario para STT, más datos = más latency
- Conversión: `scipy.signal.resample()` o `librosa.resample()`

### Formato de audio
- **PCM** (Pulse Code Modulation) — raw, sin compresión
- **WAV** — contenedor con header + PCM data
- **16-bit signed integers** — formato estándar para Whisper

### VAD (Voice Activity Detection)
- Detectar cuándo alguien empieza/deja de hablar
- Basado en energía o zero-crossing rate
- `webrtcvad` — librería eficiente para VAD

### Spectral Gating (noise reduction)
- Pasar a dominio frecuencia vía FFT
- Calcular perfil de ruido en segmentos silenciosos
- Aplicar gate espectral para atenuar ruido
- `noisereduce` (Python) — implementación lista

## FFT (Fast Fourier Transform)

```python
import numpy as np

def fft_spectrum(audio: np.ndarray, sample_rate: int) -> tuple:
    """Retorna frecuencias y magnitudes FFT"""
    n = len(audio)
    freqs = np.fft.rfftfreq(n, d=1/sample_rate)
    magnitudes = np.abs(np.fft.rfft(audio))
    return freqs, magnitudes
```

## Wake Word Detection (openwakeword)

```python
from openwakeword import Model

# Cargar modelo custom "YARTIS"
oww = Model(wakeword_models=["models/yartis.tflite"])

# Detectar en chunks de audio
predictions = oww.predict(audio_chunk)
if predictions["yartis"] > 0.5:
    print("Wake word detectada!")
```

## Whisper STT

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.wav", language="es")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## Recording con detección de silencio

```python
import pyaudio
import numpy as np
import webrtcvad

CHUNK = 1600       # 100ms @ 16kHz
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_SECS = 1.5  # segundos de silencio para cortar

vad = webrtcvad.Vad(2)  # agresividad 0-3

def record_until_silence():
    p = pyaudio.PyAudio()
    stream = p.open(FORMAT, CHANNELS, RATE, True, CHUNK, 
                    frames_per_buffer=CHUNK)
    
    frames = []
    silence_chunks = 0
    silence_threshold = int(SILENCE_SECS * RATE / CHUNK)
    
    while silence_chunks < silence_threshold:
        data = stream.read(CHUNK)
        frames.append(data)
        
        # VAD: es voz o silencio?
        if vad.is_speech(data, RATE):
            silence_chunks = 0
        else:
            silence_chunks += 1
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)
```

## Noise reduction con noisereduce

```python
import noisereduce as nr
import numpy as np

def reduce_noise(audio: np.ndarray, sample_rate: int) -> np.ndarray:
    """Reduce ruido de fondo usando spectral gating"""
    return nr.reduce_noise(
        y=audio,
        sr=sample_rate,
        prop_decrease=0.8,    # qué tanto reducir
        n_fft=512,            # ventana FFT
        stationary=True       # ruido estacionario vs no-estacionario
    )
```

## Buffers circulares (Rust)

```rust
// Buffer circular para audio en Rust
struct CircularBuffer {
    buffer: Vec<f32>,
    size: usize,
    write_pos: usize,
}

impl CircularBuffer {
    fn new(size: usize) -> Self {
        Self {
            buffer: vec![0.0; size],
            size,
            write_pos: 0,
        }
    }

    fn push(&mut self, samples: &[f32]) {
        for &sample in samples {
            self.buffer[self.write_pos] = sample;
            self.write_pos = (self.write_pos + 1) % self.size;
        }
    }

    fn contents(&self) -> Vec<f32> {
        // Retorna en orden cronológico
        let mut result = Vec::with_capacity(self.size);
        result.extend_from_slice(&self.buffer[self.write_pos..]);
        result.extend_from_slice(&self.buffer[..self.write_pos]);
        result
    }
}
```

## Herramientas CLI útiles

```bash
# Ver dispositivos de audio
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"

# Probar grabación rápida
ffmpeg -f dshow -i audio="Micrófono" -t 5 test.wav

# Ver info de un WAV
ffprobe test.wav
```
