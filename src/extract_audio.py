import subprocess
import os
from tqdm import tqdm

def extract_audio(video_path, output_dir):
    audio_file = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + ".wav")
    
    # Get duration
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ]
    duration = float(subprocess.check_output(cmd).decode().strip())

    # Run ffmpeg
    cmd_ffmpeg = [
        "ffmpeg", "-y", "-i", video_path, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_file,
        "-progress", "pipe:1"
    ]
    process = subprocess.Popen(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pbar = tqdm(total=duration, unit="s", desc="Audio Extraction", dynamic_ncols=True)

    for line in process.stdout:
        if "out_time_ms=" in line:
            out_time = int(line.strip().split("=")[1])
            pbar.n = out_time / 1_000_000
            pbar.refresh()
    process.wait()
    pbar.n = duration
    pbar.refresh()
    pbar.close()
    return audio_file
