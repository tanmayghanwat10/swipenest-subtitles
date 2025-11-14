import os
import sys
import time
import multiprocessing as mp
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Use absolute imports
from src.extract_audio import extract_audio
from src.generate_subtitles import generate_subtitles

VIDEO_EXTS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv")

def parse_config(config_path: Path):
    cfg = {}
    if not config_path.exists():
        print(f"⚠️ Config not found at {config_path}, using defaults.")
        return {"INPUT_DIR": "./input", "OUTPUT_DIR": "./output", "AUDIO_FORMAT": "wav", "MODEL": "tiny", "LANGUAGE": "en"}
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line or line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    cfg.setdefault("INPUT_DIR", "./input")
    cfg.setdefault("OUTPUT_DIR", "./output")
    cfg.setdefault("AUDIO_FORMAT", "wav")
    cfg.setdefault("MODEL", "tiny")
    cfg.setdefault("BEAM_SIZE", "5")
    cfg.setdefault("PATIENCE", "1.0")
    cfg.setdefault("LANGUAGE", "en")
    return cfg

def process_single_video(args):
    file_path, output_dir, audio_fmt, model_name, beam_size, patience, language = args
    print(f"\n🎥 Processing: {file_path.name}")
    start = time.time()
    try:
        # Load model inside the process to avoid pickling issues
        from faster_whisper import WhisperModel
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        audio_path = extract_audio(str(file_path), str(output_dir), fmt=audio_fmt)
        _ = generate_subtitles(audio_path, str(output_dir), model, language=language, beam_size=beam_size, patience=patience)
        success = True
        error = None
    except Exception as e:
        success = False
        error = str(e)
        print(f"❌ Error processing {file_path.name}: {e}")
    end = time.time()
    elapsed = end - start
    minutes, seconds = divmod(elapsed, 60)
    print(f"⏱️ File time: {elapsed:.2f}s ({int(minutes)}m {int(seconds)}s)")
    return success, elapsed, error

def process_local_videos():
    base_dir = Path(__file__).resolve().parent.parent
    config = parse_config(base_dir / "Config.txt")

    input_dir = Path(config["INPUT_DIR"]).resolve()
    output_dir = Path(config["OUTPUT_DIR"]).resolve()
    audio_fmt = config["AUDIO_FORMAT"].lower()
    model_name = config["MODEL"]
    beam_size = int(config["BEAM_SIZE"])
    patience = float(config["PATIENCE"])
    language = config["LANGUAGE"]

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Input folder: {input_dir}")
    print(f"📂 Output folder: {output_dir}")
    print(f"🔧 Audio format: {audio_fmt} | Model: {model_name} | Language: {language}")

    total_start = time.time()
    processed = 0
    successful = 0
    total_time = 0

    # Collect video files
    video_files = [f for f in sorted(input_dir.iterdir()) if f.is_file() and f.suffix.lower() in VIDEO_EXTS]
    if not video_files:
        print("No video files found in input directory.")
        return

    # Use ProcessPoolExecutor for parallel processing
    max_workers = min(mp.cpu_count(), len(video_files))
    print(f"🚀 Processing {len(video_files)} videos with {max_workers} parallel workers.")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = [executor.submit(process_single_video, (file, output_dir, audio_fmt, model_name, beam_size, patience, language)) for file in video_files]

        # Collect results
        for future in as_completed(futures):
            processed += 1
            success, elapsed, error = future.result()
            if success:
                successful += 1
            total_time += elapsed

    total_end = time.time()
    total_elapsed = total_end - total_start
    tmin, tsec = divmod(total_elapsed, 60)
    print(f"\n✅ Completed. Files processed: {processed}, Successful: {successful}")
    print(f"⏱️ Total processing time: {total_elapsed:.2f}s ({int(tmin)}m {int(tsec)}s)")
    print(f"⏱️ Average time per file: {total_time / processed:.2f}s")

def main():
    process_local_videos()

if __name__ == "__main__":
    main()
    