import logging
import os
import sys
import time
import multiprocessing as mp
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Tuple

# Use absolute imports
from src.extract_audio import extract_audio
from src.generate_subtitles import generate_subtitles

VIDEO_EXTS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_config(config_path: Path) -> Dict[str, str]:
    """
    Parses the configuration file and returns a dictionary of settings.

    Args:
        config_path (Path): Path to the configuration file.

    Returns:
        Dict[str, str]: Configuration dictionary with default values.
    """
    cfg: Dict[str, str] = {}
    if not config_path.exists():
        logger.warning(f"Config not found at {config_path}, using defaults.")
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

def process_single_video(args: Tuple[Path, Path, str, str, int, float, str]) -> Tuple[bool, float, str]:
    """
    Processes a single video file: extracts audio and generates subtitles.

    Args:
        args (Tuple): Contains file_path, output_dir, audio_fmt, model_name, beam_size, patience, language.

    Returns:
        Tuple[bool, float, str]: Success status, elapsed time, and error message if any.
    """
    file_path, output_dir, audio_fmt, model_name, beam_size, patience, language = args
    logger.info(f"Processing: {file_path.name}")
    start = time.time()
    try:
        # Load model inside the process to avoid pickling issues
        from faster_whisper import WhisperModel
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        audio_path = extract_audio(str(file_path), str(output_dir), fmt=audio_fmt)
        _ = generate_subtitles(audio_path, str(output_dir), model, language=language, beam_size=beam_size, patience=patience)
        success = True
        error = ""
    except Exception as e:
        success = False
        error = str(e)
        logger.error(f"Error processing {file_path.name}: {e}")
    end = time.time()
    elapsed = end - start
    minutes, seconds = divmod(elapsed, 60)
    logger.info(f"File time: {elapsed:.2f}s ({int(minutes)}m {int(seconds)}s)")
    return success, elapsed, error

def process_local_videos(input_dir: Path = None) -> None:
    """
    Processes all video files in the input directory using parallel execution.

    Args:
        input_dir (Path): Optional input directory path. If None, uses config.
    """
    base_dir = Path(__file__).resolve().parent.parent
    config = parse_config(base_dir / "Config.txt")

    if input_dir is None:
        input_dir = Path(config["INPUT_DIR"]).resolve()
    output_dir = Path(config["OUTPUT_DIR"]).resolve()
    audio_fmt = config["AUDIO_FORMAT"].lower()
    model_name = config["MODEL"]
    beam_size = int(config["BEAM_SIZE"])
    patience = float(config["PATIENCE"])
    language = config["LANGUAGE"]

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Input folder: {input_dir}")
    logger.info(f"Output folder: {output_dir}")
    logger.info(f"Audio format: {audio_fmt} | Model: {model_name} | Language: {language}")

    total_start = time.time()
    processed = 0
    successful = 0
    total_time = 0.0

    # Collect video files
    video_files: List[Path] = [f for f in sorted(input_dir.iterdir()) if f.is_file() and f.suffix.lower() in VIDEO_EXTS]
    if not video_files:
        logger.warning("No video files found in input directory.")
        return

    # Use ProcessPoolExecutor for parallel processing
    max_workers = min(mp.cpu_count(), len(video_files))
    logger.info(f"Processing {len(video_files)} videos with {max_workers} parallel workers.")

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
    logger.info(f"Completed. Files processed: {processed}, Successful: {successful}")
    logger.info(f"Total processing time: {total_elapsed:.2f}s ({int(tmin)}m {int(tsec)}s)")
    if processed > 0:
        logger.info(f"Average time per file: {total_time / processed:.2f}s")

def download_youtube_video(url: str, output_dir: Path) -> Path:
    """
    Downloads a YouTube video using yt-dlp and returns the path to the downloaded file.

    Args:
        url (str): YouTube URL to download.
        output_dir (Path): Directory to save the downloaded video.

    Returns:
        Path: Path to the downloaded video file.

    Raises:
        RuntimeError: If download fails.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "%(title)s.%(ext)s")

    logger.info(f"Downloading YouTube video from {url}")
    try:
        import yt_dlp
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'best[height<=720]',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            video_file = Path(filename)
    except Exception as e:
        raise RuntimeError(f"yt-dlp download failed: {e}")

    if not video_file.exists():
        raise RuntimeError("No video file was downloaded.")

    logger.info(f"Downloaded video: {video_file}")
    return video_file

def process_youtube_url(url: str) -> None:
    """
    Processes a YouTube URL: downloads the video and generates subtitles.

    Args:
        url (str): YouTube URL to process.
    """
    base_dir = Path(__file__).resolve().parent.parent
    config = parse_config(base_dir / "Config.txt")

    temp_dir = base_dir / "input" / "temp_youtube"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Download the video
        video_path = download_youtube_video(url, temp_dir)

        # Process the downloaded video
        process_local_videos(temp_dir)

    finally:
        # Clean up temporary files
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            logger.info("Cleaned up temporary YouTube download files.")

def main() -> None:
    """
    Main entry point of the application.
    """
    print("Welcome to Swipenest Subtitles Generator!")
    print("Choose an option:")
    print("1. Process local videos from input/Local_Videos/")
    print("2. Process a YouTube URL")

    while True:
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice == "1":
                process_local_videos()
                break
            elif choice == "2":
                url = input("Enter YouTube URL: ").strip()
                if url:
                    process_youtube_url(url)
                    break
                else:
                    print("Please enter a valid URL.")
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
