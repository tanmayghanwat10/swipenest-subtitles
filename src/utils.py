import torch
import whisper

def load_whisper_model():
    if torch.cuda.is_available():
        print("GPU detected ::: using whisper-medium")
        model = whisper.load_model("medium").to("cuda")
        device = "cuda"
    else:
        print("CPU detected ::: using whisper-tiny")
        model = whisper.load_model("tiny")
        device = "cpu"

    return model, device
