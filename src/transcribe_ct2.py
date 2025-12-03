from faster_whisper import WhisperModel
import os

def generate_subtitles(audio_path, output_dir):
    print("📥 Loading Faster-Whisper model (medium, multi-lingual)...")

    model = WhisperModel(
        "medium",
        device="cpu",
        compute_type="int8",
        download_root="models"
    )

    segments, _ = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True,
        language=None  # auto-detect
    )

    srt_path = os.path.join(output_dir, "subtitles.srt")

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            f.write(f"{i}\n")
            f.write(f"{seg.start:.2f} --> {seg.end:.2f}\n")
            f.write(f"{seg.text.strip()}\n\n")

    return srt_path
