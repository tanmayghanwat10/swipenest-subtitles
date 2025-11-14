import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

def _format_time_srt(t: float) -> str:
    """
    Formats a time in seconds to SRT timestamp format.

    Args:
        t (float): Time in seconds.

    Returns:
        str: Formatted time string.
    """
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_subtitles(audio_path: str, output_dir: str, model: Any, language: str = "en", beam_size: int = 5, patience: float = 1.0) -> str:
    """
    Generates subtitles from an audio file using the provided model.

    Args:
        audio_path (str): Path to the audio file.
        output_dir (str): Directory to save the subtitle file.
        model (Any): The Whisper model instance.
        language (str): Language for transcription.
        beam_size (int): Beam size for decoding.
        patience (float): Patience for decoding.

    Returns:
        str: Path to the generated subtitle file.
    """
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    subtitle_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.srt"))

    logger.info(f"Generating subtitles from {audio_path} -> {subtitle_path}")
    segments, info = model.transcribe(audio_path, language=language if language != "auto" else None, vad_filter=True, beam_size=beam_size, patience=patience)  # Enable VAD for better accuracy, auto-detect language if set to auto

    with open(subtitle_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = _format_time_srt(segment.start)
            end = _format_time_srt(segment.end)
            text = segment.text.strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    logger.info(f"Subtitles saved at: {subtitle_path}")
    return subtitle_path
