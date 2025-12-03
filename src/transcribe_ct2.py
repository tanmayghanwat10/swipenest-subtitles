from faster_whisper import WhisperModel
from tqdm import tqdm
import os
import soundfile as sf

def generate_subtitles(audio_path, output_dir):
    output_file = os.path.join(output_dir, "subtitles.srt")
    model = WhisperModel("medium", device="cpu")  # Change device="cuda" for GPU

    duration = sf.SoundFile(audio_path).frames / sf.SoundFile(audio_path).samplerate
    segments, _ = model.transcribe(audio_path, beam_size=5, language="en", word_timestamps=True)

    pbar = tqdm(total=duration, unit="s", desc="Subtitle Generation", dynamic_ncols=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"{segment.index}\n{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n{segment.text}\n\n")
            pbar.n = segment.end
            pbar.refresh()
    pbar.n = duration
    pbar.refresh()
    pbar.close()
    return output_file

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
