import os

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def list_videos(directory):
    return [
        f for f in os.listdir(directory)
        if f.lower().endswith((".mp4", ".mkv", ".mov", ".avi"))
    ]
