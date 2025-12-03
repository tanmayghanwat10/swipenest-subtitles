import os
import argparse
import time
from tqdm import tqdm
from extract_audio import extract_audio
from transcribe_ct2 import generate_subtitles  # assuming this is your transcription function

def process_video(video_path, output_dir):
    video_name = os.path.basename(video_path)
    print(f"\n🎬 Processing: {video_name}")
    start_video = time.time()

    # Step 1: Audio extraction
    print("✔ Extracting audio...")
    audio_path = extract_audio(video_path, output_dir)

    # Step 2: Subtitles generation
    print("📝 Generating subtitles...")
    subtitles_path = generate_subtitles(audio_path, output_dir)

    end_video = time.time()
    print(f"✅ Finished {video_name} in {round(end_video - start_video, 2)} seconds")
    return end_video - start_video

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    videos = [f for f in os.listdir(input_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]

    if not videos:
        raise FileNotFoundError(f"No videos found in {input_dir}")

    total_videos = len(videos)
    print(f"🚀 Found {total_videos} video(s). Starting processing...\n")
    start_all = time.time()

    for idx, video in enumerate(videos, start=1):
        print(f"📌 Overall Progress: Video {idx}/{total_videos}")
        process_video(os.path.join(input_dir, video), output_dir)

        elapsed = time.time() - start_all
        avg_time = elapsed / idx
        remaining = avg_time * (total_videos - idx)
        print(f"⏱ Total elapsed: {round(elapsed,2)}s | Estimated remaining: {round(remaining,2)}s\n")

    end_all = time.time()
    print(f"🎉 All {total_videos} videos processed in {round(end_all - start_all,2)} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="/app/input")
    parser.add_argument("--output_dir", type=str, default="/app/output")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
