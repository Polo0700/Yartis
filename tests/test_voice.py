"""Test de la huella vocal (voice_id / ECAPA).

Verifica que my_voice.pt (creado con extract_voice.py) reconoce la voz
de Jorge y rechaza voces diferentes.

Uso: pytest tests/test_voice.py -v
"""
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""

import shutil
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

import speechbrain.utils.fetching as fetching

# Parche Windows: speechbrain intenta symlinks (WinError 1314) -> copiar
def _link_with_strategy(src, dst, strategy="copy"):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


fetching.link_with_strategy = _link_with_strategy

from speechbrain.inference.speaker import EncoderClassifier

RAIZ = Path(__file__).parent.parent
UMBRAL = 0.65  # mismo umbral que voice_id.py

MODELO = RAIZ / "pretrained_models" / "spkrec-ecapa-voxceleb"
MI_VOZ = RAIZ / "my_voice.pt"
JORGE = RAIZ / "assets" / "jorge.wav"


def _cargar_classifier():
    return EncoderClassifier.from_hparams(
        source=str(MODELO),
        savedir=str(MODELO),
        run_opts={"device": "cpu"},
    )


def _embedding_de(audio_path):
    data, _ = sf.read(audio_path)
    audio = data.astype(np.float32)
    tensor = torch.from_numpy(audio)
    if tensor.dim() == 1:
        tensor = tensor.unsqueeze(0)
    return tensor


def _similitud(classifier, audio_tensor, referencia):
    emb = classifier.encode_batch(audio_tensor).flatten()
    ref = referencia.flatten()
    return torch.nn.functional.cosine_similarity(emb, ref, dim=0).item()


def test_my_voice_existe():
    assert MI_VOZ.exists(), "Falta my_voice.pt (ejecuta: python extract_voice.py assets/jorge.wav)"


def test_jorge_se_reconoce():
    """La voz que creó la huella debe superar el umbral."""
    classifier = _cargar_classifier()
    referencia = torch.load(MI_VOZ)
    score = _similitud(classifier, _embedding_de(JORGE), referencia)
    print(f"\n  similitud jorge.wav vs my_voice.pt: {score:.3f} (umbral {UMBRAL})")
    assert score > UMBRAL, f"Debía reconocer a Jorge, dio {score:.3f}"


def test_voz_diferente_se_rechaza():
    """Las voces de ejemplo del modelo deben dar similitud baja."""
    classifier = _cargar_classifier()
    referencia = torch.load(MI_VOZ)
    ejemplos = [
        MODELO / "example1.wav",
        MODELO / "example2.flac",
    ]
    for ejemplo in ejemplos:
        if not ejemplo.exists():
            continue
        score = _similitud(classifier, _embedding_de(ejemplo), referencia)
        print(f"\n  similitud {ejemplo.name} vs my_voice.pt: {score:.3f} (umbral {UMBRAL})")
        assert score < UMBRAL, f"Rechazó mal: {ejemplo.name} dio {score:.3f}"
