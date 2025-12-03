import os
import argparse
import time
from tqdm import tqdm
from extract_audio import extract_audio
from generate_subtitles import generate_subtitles

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Get all video files
    videos = [f for f in os.listdir(input_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]
    if not videos:
        raise FileNotFoundError(f"❌ No videos found in {input_dir} folder.")

    total_videos = len(videos)
    print(f"🚀 Found {total_videos} video(s) in {input_dir}. Starting processing...\n")

    start_all = time.time()

    for idx, video in enumerate(videos, start=1):
        video_path = os.path.join(input_dir, video)
        print(f"🎬 Processing [{idx}/{total_videos}]: {video}")

        start_video = time.time()

        # Simulate step progress using tqdm
        steps = ["Extracting audio", "Generating subtitles"]
        for step in tqdm(steps, desc=f"{video} progress", unit="step"):
            if step == "Extracting audio":
                extract_audio(video_path, output_dir)
            elif step == "Generating subtitles":
                generate_subtitles(os.path.join(output_dir, os.path.splitext(video)[0] + ".wav"), output_dir)

        end_video = time.time()
        print(f"✅ Finished {video} in {round(end_video - start_video, 2)} seconds.\n")

        # Show approximate overall progress
        elapsed = end_video - start_all
        avg_time = elapsed / idx
        remaining = avg_time * (total_videos - idx)
        print(f"⏱ Elapsed: {round(elapsed,2)}s | Estimated remaining: {round(remaining,2)}s\n")

    end_all = time.time()
    print(f"🎉 All {total_videos} videos processed in {round(end_all - start_all,2)} seconds.")
