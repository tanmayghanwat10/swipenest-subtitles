import sys
sys.path.append("src")

import os
import time
import logging
from extract_audio import extract_audio
from generate_subtitles import generate_subtitles

INPUT_DIR = "input"
OUTPUT_DIR = "output"

VIDEO_EXTENSIONS = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

def select_video(videos):
    logger.info("Multiple videos detected:")
    for idx, video in enumerate(videos, start=1):
        print(f"{idx}. {video}")

    while True:
        try:
            choice = int(input("Enter the number of the video to process: "))
            if 1 <= choice <= len(videos):
                return videos[choice - 1]
            else:
                logger.warning("Invalid number selected")
        except ValueError:
            logger.warning("Please enter a valid number")

def main():
    start_time = time.time()
    logger.info("Subtitle generation started")

    if not os.path.exists(INPUT_DIR):
        logger.error("input/ folder not found")
        return

    videos = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(VIDEO_EXTENSIONS)
    ]

    if not videos:
        logger.error("No video files found in input/ folder")
        return

    if len(videos) == 1:
        selected_video = videos[0]
        logger.info(f"Single video detected: {selected_video}")
    else:
        selected_video = select_video(videos)

    video_path = os.path.join(INPUT_DIR, selected_video)
    logger.info(f"Processing video: {selected_video}")

    try:
        audio = extract_audio(video_path, OUTPUT_DIR)
        generate_subtitles(audio, OUTPUT_DIR)
        logger.info("Subtitle generation completed successfully")
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        return

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    logger.info(f"Total execution time: {elapsed} seconds")

if __name__ == "__main__":
    main()
