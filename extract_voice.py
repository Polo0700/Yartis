"""Extrae la huella vocal (embedding ECAPA) de un audio y la guarda en my_voice.pt.

Uso: python extract_voice.py <audio.wav>
"""
import sys
import shutil
from pathlib import Path

# --- Parche: speechbrain en Windows no puede crear symlinks (WinError 1314).
#     En vez de symlink, copiamos el archivo. ---
import speechbrain.utils.fetching as fetching


def _link_with_strategy(src, dst, strategy="copy"):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if strategy == "copy":
        shutil.copy2(src, dst)
    else:
        # fallback seguro: siempre copia
        shutil.copy2(src, dst)


fetching.link_with_strategy = _link_with_strategy

import soundfile as sf
import numpy as np
import torch
from speechbrain.inference.speaker import EncoderClassifier


def main(audio_path: str):
    print("Cargando ECAPA (local)...", flush=True)
    classifier = EncoderClassifier.from_hparams(
        source="pretrained_models/spkrec-ecapa-voxceleb",
        savedir="pretrained_models/spkrec-ecapa-voxceleb",
        run_opts={"device": "cpu"},
    )

    data, sr = sf.read(audio_path)
    print(f"Audio: {sr}Hz, {len(data)/sr:.1f}s", flush=True)

    audio = data.astype(np.float32)
    tensor = torch.from_numpy(audio)
    if tensor.dim() == 1:
        tensor = tensor.unsqueeze(0)
    embeddings = classifier.encode_batch(tensor)
    print(f"Embedding shape: {tuple(embeddings.shape)}", flush=True)
    torch.save(embeddings, "my_voice.pt")
    print("HUELLA GUARDADA: my_voice.pt", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/jorge.wav")
