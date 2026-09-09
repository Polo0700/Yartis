import yt_dlp
import sounddevice as sd
import numpy as np
import wave
import os
import sys
import tempfile
import pathlib
import soundfile as sf

nombreCancion = input("Enter the name of the song you want to download and play: ")
DOWNLOAD_DIR = pathlib.Path("assets") / "canciones"
DOWNLOAD_DIR.mkdir(exist_ok=True)
if not DOWNLOAD_DIR.exists():
    print(f"Error: Download directory {DOWNLOAD_DIR} does not exist.")
    sys.exit(1)
if not os.access(DOWNLOAD_DIR, os.W_OK):
    print(f"Error: Download directory {DOWNLOAD_DIR} is not writable.")
    sys.exit(1)
audio = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    "quiet": True,
    "nooverwrite": True,
}
with yt_dlp.YoutubeDL(audio) as ydl:
    info = ydl.extract_info(f"ytsearch:{nombreCancion}", download=True)
    entry = info["entries"][0]
    filename = entry["requested_downloads"][0]["filepath"]
    print(f"Downloaded audio info: {info}")
    print(f"Existe?: {pathlib.Path(filename).exists()}")
    print(f"Downloaded audio file: {filename}")
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()
