# 🎬 swipenest_subtitles Subtitles Generator

Automatically generate subtitles for any video using **OpenAI Whisper** and **FFmpeg**.

---

## 🚀 Features
- Accepts any video format (MP4, MKV, AVI, MOV, etc.)
- Supports YouTube URLs via .url files (downloads best format <=720p for speed)
- Extracts audio automatically using FFmpeg
- Generates accurate subtitles using Whisper
- Exports `.srt` subtitle files
- Works in both local and Docker environments
- Tanmay Ghanwat

## 📋 Requirements
- Docker (for containerized usage)
- Or Python 3.8+, FFmpeg, yt-dlp (for local usage)

## 🛠️ Installation

### Docker Installation (Recommended)
No local installation required. Simply build and run the Docker image as described in the Docker Usage section.

### Local Installation (Optional)
If running without Docker:

1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ffmpeg -version

   ```

### Run Locally 

✅ Local Run

Place video(s) inside the input/ folder

Run:
```bash
python src/main.py
```

If one video exists → processing starts automatically

If multiple videos exist → you are prompted to choose

Generated subtitles will appear in:

output/subtitles.srt

## 🐳 Docker Usage

### Initial Build

```bash
docker build -t swipenest_subtitles .
```

### Run Container

# Running Docker image

**Windows PowerShell:**

```bash
docker run -it --rm `
  -v "${PWD}\input:/app/input" `
  -v "${PWD}\output:/app/output" `
  swipenest_subtitles
```

**Linux / macOS:**
```bash
docker run -it --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  swipenest_subtitles
```

**Note:** Docker containers are immutable. To update code changes:
1. Rebuild the image (step 2 above) - dependencies are cached, only code layer rebuilds
2. Remove old container: `docker rm swipenest_subtitles_container`
3. Run the container again with the new image

## ⚙️ Configuration
- AUDIO_FORMAT: Audio format (wav/mp3)
- MODEL: Whisper model (tiny/base/small/medium/large)
- LANGUAGE: Language code (en, es, fr, etc.) or 'auto' for automatic detection
