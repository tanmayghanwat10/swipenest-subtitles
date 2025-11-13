import os
import subprocess
from pathlib import Path

def extract_audio(video_path, output_dir, fmt="wav"):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_ext = "wav" if fmt.lower() == "wav" else "mp3"
    audio_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.{audio_ext}"))

    print(f"🎧 Extracting audio from {video_path} -> {audio_path}")

    # Prefer WAV mono 16kHz for STT stability
    if audio_ext == "wav":
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", audio_path]
    else:
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "mp3", audio_path]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg audio extraction failed:\n{proc.stderr}")

    print(f"✅ Audio saved at: {audio_path}")
    return audio_path
