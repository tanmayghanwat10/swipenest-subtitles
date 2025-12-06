import os
from utils import load_whisper_model

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def generate_subtitles(audio_path, output_dir):
    model, device = load_whisper_model()

    print("Transcribing...")
    result = model.transcribe(audio_path)

    srt_path = os.path.join(output_dir, "subtitles.srt")

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")

    print(f"Subtitles saved → {srt_path}")

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
