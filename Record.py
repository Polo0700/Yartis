import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import sys

RATE = 16000
CHUNK = 1024

umbral_silencio = 500
Pasos_silencio = 0
silencio_detectado = False

model = WhisperModel("base", device="cuda", compute_type="int8_float16")

print("Recording...")

try:
    with sd.InputStream(
        samplerate=RATE, channels=1, blocksize=CHUNK, dtype="int16"
    ) as stream:
        while True:
            audio_chunk, overflow = stream.read(CHUNK)
            volume = np.abs(audio_chunk).mean()
            if volume < umbral_silencio:
                Pasos_silencio += 1
                if Pasos_silencio >= 10 and not silencio_detectado:
                    print("\nSilence detected. Transcribing...")
                    silencio_detectado = True
                    audio_data = np.concatenate((audio_chunk, stream.read(RATE * 5)[0]))
                    audio_data = audio_data.flatten().astype(np.float32) / 32768.0
                    segments, info = model.transcribe(audio_data, beam_size=5)
                    for segment in segments:
                        print(
                            f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}"
                        )
            else:
                Pasos_silencio = 0
                silencio_detectado = False

            barrita = "█" * int(volume / 30)
            sys.stdout.write(f"\rVolume: {int(volume)} {barrita:<50}")
            sys.stdout.flush()
except KeyboardInterrupt:
    print("\nRecording stopped.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
