import os
from pathlib import Path

def _format_time_srt(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_subtitles(audio_path, output_dir, model, language="en", beam_size=5, patience=1.0):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    subtitle_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.srt"))

    print(f"📝 Generating subtitles from {audio_path} -> {subtitle_path}")
    segments, info = model.transcribe(audio_path, language=language if language != "auto" else None, vad_filter=True, beam_size=beam_size, patience=patience)  # Enable VAD for better accuracy, auto-detect language if set to auto

    with open(subtitle_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = _format_time_srt(segment.start)
            end = _format_time_srt(segment.end)
            text = segment.text.strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"✅ Subtitles saved at: {subtitle_path}")
    return subtitle_path
