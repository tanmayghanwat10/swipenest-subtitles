import os
from pathlib import Path
import whisper

def _format_time_srt(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_subtitles(audio_path, output_dir, model_name="tiny", language="en"):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    subtitle_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.srt"))

    print(f"📝 Generating subtitles from {audio_path} -> {subtitle_path}")
    model = whisper.load_model(model_name)  # "tiny" or "base"
    result = model.transcribe(audio_path, fp16=False, language=language)

    with open(subtitle_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], start=1):
            start = _format_time_srt(seg["start"])
            end = _format_time_srt(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"✅ Subtitles saved at: {subtitle_path}")
    return subtitle_path
