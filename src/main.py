import os
import time
from pathlib import Path
# Instead of relative imports
# from .extract_audio import extract_audio
# from .generate_subtitles import generate_subtitles

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
    cfg.setdefault("LANGUAGE", "en")
    return cfg

def main():
    base_dir = Path(__file__).resolve().parent.parent
    config = parse_config(base_dir / "Config.txt")

    input_dir = Path(config["INPUT_DIR"]).resolve()
    output_dir = Path(config["OUTPUT_DIR"]).resolve()
    audio_fmt = config["AUDIO_FORMAT"].lower()
    model_name = config["MODEL"]
    language = config["LANGUAGE"]

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Input folder: {input_dir}")
    print(f"📂 Output folder: {output_dir}")
    print(f"🔧 Audio format: {audio_fmt} | Model: {model_name} | Language: {language}")

    total_start = time.time()
    processed = 0

    for file in sorted(input_dir.iterdir()):
        if file.is_file() and file.suffix.lower() in VIDEO_EXTS:
            processed += 1
            print(f"\n🎥 Processing: {file.name}")
            start = time.time()
            try:
                audio_path = extract_audio(str(file), str(output_dir), fmt=audio_fmt)
                _ = generate_subtitles(audio_path, str(output_dir), model_name=model_name, language=language)
            except Exception as e:
                print(f"❌ Error processing {file.name}: {e}")
            end = time.time()
            elapsed = end - start
            minutes, seconds = divmod(elapsed, 60)
            print(f"⏱️ File time: {elapsed:.2f}s ({int(minutes)}m {int(seconds)}s)")

    total_end = time.time()
    total_elapsed = total_end - total_start
    tmin, tsec = divmod(total_elapsed, 60)
    print(f"\n✅ Completed. Files processed: {processed}")
    print(f"⏱️ Python total time: {total_elapsed:.2f}s ({int(tmin)}m {int(tsec)}s)")

if __name__ == "__main__":
    main()
