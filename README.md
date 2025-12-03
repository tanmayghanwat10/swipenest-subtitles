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
   ```

## 🐳 Docker Usage

### Initial Build

```bash
docker build -t swipenest_subtitles .
```

### Rebuild image after code changes (fast - uses cached dependencies)

```bash
docker build -t swipenest_subtitles .
```

### Run Container

# Running Docker image>>>>>>....(TRY THIS)

**Windows PowerShell:**

```bash
docker run -it --rm `  -v "${PWD}\input:/app/input" `  -v "${PWD}\output:/app/output" `  swipenest_subtitles
```

**Linux / macOS:**
```bash
# Stop existing container (keeps it for reuse)
docker stop swipenest_subtitles_container 2>/dev/null

# Restart or create new container with fresh mounts
docker start swipenest_subtitles_container 2>/dev/null || docker run -it --name swipenest_subtitles_container -v $(pwd)/input/Local_Videos:/app/input -v $(pwd)/output:/app/output swipenest_subtitles
```

**Note:** Docker containers are immutable. To update code changes:
1. Rebuild the image (step 2 above) - dependencies are cached, only code layer rebuilds
2. Remove old container: `docker rm swipenest_subtitles_container`
3. Run the container again with the new image

### Quick update one-liner (rebuild + restart)

**Linux/macOS:**
```bash
docker build -t swipenest_subtitles . && docker rm -f swipenest_subtitles_container 2>/dev/null; 
docker rm -f swipenest_subtitles_container && docker run -it --name swipenest_subtitles_container -v $(pwd)/input/Local_Videos:/app/input -v $(pwd)/output:/app/output swipenest_subtitles
```

**Windows PowerShell:**
```powershell
docker build -t swipenest_subtitles . ; docker rm -f swipenest_subtitles_container 2>$null ; docker rm -f swipenest_subtitles_container && docker run -it --name swipenest_subtitles_container -v $(pwd)/input/Local_Videos:/app/input -v $(pwd)/output:/app/output swipenest_subtitles
```
## ⚙️ Configuration
Edit `Config.txt` to customize:
- INPUT_DIR: Input directory path
- OUTPUT_DIR: Output directory path
- AUDIO_FORMAT: Audio format (wav/mp3)
- MODEL: Whisper model (tiny/base/small/medium/large)
- LANGUAGE: Language code (en, es, fr, etc.) or 'auto' for automatic detection
