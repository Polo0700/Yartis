import os
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import yt_dlp


class music:
    def __init__(self):
        self.volumen_actual = 1.0
        self.cola = []
        self.carpeta = Path(__file__).parent.parent / "assets" / "canciones"
        self.carpeta.mkdir(exist_ok=True)
        self.stream = None
        self.position = 0
        self.pista_actual = 0
        self.data = None
        self.sr = None

    def search(self, nombreCancion):
        if not self.carpeta.exists():
            print(f"Error: Download directory {self.carpeta} does not exist.")
            return "No encontre la carpeta de canciones, favor de contactar la administracion"
        if not os.access(self.carpeta, os.W_OK):
            print(f"Error: Download directory {self.carpeta} is not writable.")
            return "no tengo acceso a la carpeta de canciones, favor de contactar la administracion"
        audio = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": str(self.carpeta / "%(title)s.%(ext)s"),
            "quiet": True,
            "nooverwrite": True,
        }
        with yt_dlp.YoutubeDL(audio) as ydl:
            info = ydl.extract_info(f"ytsearch:{nombreCancion}", download=True)
            entry = info["entries"][0]
            filename = entry["requested_downloads"][0]["filepath"]
            print(f"Downloaded audio file: {filename}")
            self.data, self.sr = sf.read(filename)
            self.position = 0
        return filename

    def play(self, nombreCancion):
        filename = self.search(nombreCancion)
        self.playlist(filename)
        self.pista_actual = len(self.cola) - 1
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.sr, channels=2, callback=self.buffer
            )
        self.stream.start()

    def buffer(self, outdata, frames, time, status):
        frame = self.data[self.position : self.position + frames]
        chunk_len = len(frame)
        if chunk_len < frames:
            outdata[:chunk_len] = frame * self.volumen_actual
            outdata[chunk_len:] = 0
            raise sd.CallbackStop()
        else:
            outdata[:] = frame * self.volumen_actual
            self.position += frames

    def volumen(self, nivel):
        self.volumen_actual = max(0.0, min(1.0, nivel))

    def playlist(self, filename):
        self.cola.append(filename)

    def next(self):
        if self.stream is None:
            return
        if self.pista_actual + 1 < len(self.cola):
            self.stream.stop()
            self.pista_actual += 1
            filename = self.cola[self.pista_actual]
            self.data, self.sr = sf.read(filename)
            self.position = 0
            self.stream.start()

    def previously(self):
        if self.stream is None:
            return
        if self.pista_actual > 0:
            self.stream.stop()
            self.pista_actual -= 1
            filename = self.cola[self.pista_actual]
            self.data, self.sr = sf.read(filename)
            self.position = 0
            self.stream.start()

    def pause(self):
        if self.stream:
            self.stream.stop()

    def resume(self):
        if self.stream:
            self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
