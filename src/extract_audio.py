import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_audio(video_path: str, output_dir: str, fmt: str = "wav") -> str:
    """
    Extracts audio from a video file using ffmpeg.

    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory to save the audio file.
        fmt (str): Audio format ('wav' or 'mp3').

    Returns:
        str: Path to the extracted audio file.

    Raises:
        RuntimeError: If ffmpeg extraction fails.
    """
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_ext = "wav" if fmt.lower() == "wav" else "mp3"
    audio_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.{audio_ext}"))

    logger.info(f"Extracting audio from {video_path} -> {audio_path}")

    # Prefer WAV mono 16kHz for STT stability
    if audio_ext == "wav":
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", audio_path]
    else:
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "mp3", audio_path]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg audio extraction failed:\n{proc.stderr}")

    logger.info(f"Audio saved at: {audio_path}")
    return audio_path
