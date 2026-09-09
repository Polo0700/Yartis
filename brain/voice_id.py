import torch
from speechbrain.inference.speaker import EncoderClassifier


class Recognizer:
    def __init__(self):
        self.tmpdir = "pretrained_models/spkrec-ecapa-voxceleb"
        self.classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb", savedir=self.tmpdir
        )
        self.reference_audio = torch.load("my_voice.pt")

    def process(self, audio):
        tensor = torch.from_numpy(audio).float()
        tensor = torch.permute(tensor, (1, 0))
        embeddings = self.classifier.encode_batch(tensor)
        prediction = torch.nn.functional.cosine_similarity(
            embeddings, self.reference_audio
        )
        return prediction.item() > 0.65
