"""
limpiar_exit.py — Limpieza de audio sintético (OpenUtau)
=========================================================
Técnicas: EQ, compresión, reverb por convolución, fade out.
Uso:   python scripts/limpiar_exit.py
Salida: assets/Exit_main_processed.wav
"""

import soundfile as sf
import numpy as np
import scipy.signal
import librosa

# ── 1. Cargar ────────────────────────────────────────────────
data, fs = sf.read("assets/Exit_main.wav")
original = data.copy()

# ── 2. EQ (ecualización) ─────────────────────────────────────
# 2a. Reducir zona "robótica" 2kHz-5kHz con un filtro
#     Orden 2 (más suave que orden 4) para no sonar hueco
sos_robotic = scipy.signal.butter(2, [2000, 5000], btype="bandstop", fs=fs, output="sos")
data = scipy.signal.sosfilt(sos_robotic, data)

# 2b. Acentuar cuerpo de la voz 200Hz-500Hz
sos_body = scipy.signal.butter(2, 200, btype="highpass", fs=fs, output="sos")
body = scipy.signal.sosfilt(sos_body, data)
sos_body_low = scipy.signal.butter(2, 500, btype="lowpass", fs=fs, output="sos")
body = scipy.signal.sosfilt(sos_body_low, body)
# Mezclar un toque del cuerpo realzado
data = data + body * 0.08

# ── 3. Compresión suave ─────────────────────────────────────
# RMS en ventanas para detectar volumen
window = int(0.01 * fs)  # 10ms
rms = librosa.feature.rms(y=data, frame_length=window, hop_length=window//2)[0]

# target RMS más bajo para que suene más suave
target_rms = 0.14
rms_safe = np.maximum(rms, 0.001)  # evitar división por cero
gain = target_rms / rms_safe
gain = np.clip(gain, 0.5, 2.0)  # compresión suave: max 2x up, 0.5x down

# Interpolar gain a la misma longitud que data
gain_interp = np.interp(
    np.linspace(0, len(data), len(data)),
    np.linspace(0, len(data), len(gain)),
    gain
)
data = data * gain_interp

# ── 4. Reverb sutil (por convolución) ────────────────────────
# Creamos una respuesta al impulso (IR) de sala pequeña
# Ruido blanco con decaimiento exponencial de 0.15s
ir_len = int(0.15 * fs)
ir = np.random.randn(ir_len)
# Decaimiento exponencial
t = np.linspace(0, 1, ir_len)
decay = np.exp(-t * 12)  # 12 = tasa de decaimiento
ir = ir * decay
# Normalizar IR
ir = ir / np.max(np.abs(ir))

# Convolución
reverb = scipy.signal.convolve(data, ir, mode="full")[:len(data)]
# Mezclar: 90% seco, 10% reverb (sutil, no inundar)
data = data * 0.90 + reverb * 0.10

# ── 5. Fade out suave ────────────────────────────────────────
fade_len = int(0.05 * fs)  # 50ms
fade = np.linspace(1, 0, fade_len)
data[-fade_len:] *= fade

# ── 6. Normalizar y guardar ─────────────────────────────────
# Normalizar más bajo para que suene natural, no forzado
peak = np.max(np.abs(data))
target_peak = 0.65
data = data / peak * target_peak

sf.write("assets/Exit_main_processed.wav", data, fs)
print(f"[OK] Procesado guardado: assets/Exit_main_processed.wav")
print(f"   Original:     {len(original)/fs:.3f}s, {np.max(np.abs(original)):.3f} peak")
print(f"   Procesado:   {len(data)/fs:.3f}s, {np.max(np.abs(data)):.3f} peak")
print(f"   Cambio RMS:  {np.sqrt(np.mean(original**2)):.4f} → {np.sqrt(np.mean(data**2)):.4f}")
