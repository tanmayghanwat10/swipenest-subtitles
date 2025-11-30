# 🎬 Swipenest Subtitles Generator

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

## 📖 Usage

### Local Videos
Place video files in the `input/` directory and run:
```bash
python -m src.main_local
```

### YouTube Videos
Create `.url` files in the `input/` directory with YouTube URLs (one per file) and run:
```bash
python -m src.main_youtube
```

## 📋 Requirements
- Python 3.8+
- FFmpeg
- yt-dlp (for YouTube support)

## 🛠️ Installation

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
docker build -t swipenest .
```

### Rebuild image after code changes (fast - uses cached dependencies)

```bash
docker build -t swipenest .
```

### Run Container

**Windows PowerShell:**
```powershell
# Stop existing container (keeps it for reuse)
docker stop swipenest_container 2>$null

# Restart or create new container with fresh mounts
docker start swipenest_container 2>$null || docker run -it --name swipenest_container -v ${PWD}\input:/app/input -v ${PWD}\output:/app/output swipenest
```

**Linux / macOS:**
```bash
# Stop existing container (keeps it for reuse)
docker stop swipenest_container 2>/dev/null

# Restart or create new container with fresh mounts
docker start swipenest_container 2>/dev/null || docker run -it --name swipenest_container -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output swipenest
```

**Note:** Docker containers are immutable. To update code changes:
1. Rebuild the image (step 2 above) - dependencies are cached, only code layer rebuilds
2. Remove old container: `docker rm swipenest_container`
3. Run the container again with the new image

### Quick update one-liner (rebuild + restart)

**Linux/macOS:**
```bash
docker build -t swipenest . && docker rm -f swipenest_container 2>/dev/null; docker run -it --name swipenest_container -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output swipenest
```

**Windows PowerShell:**
```powershell
docker build -t swipenest . ; docker rm -f swipenest_container 2>$null ; docker run -it --name swipenest_container -v ${PWD}\input:/app/input -v ${PWD}\output:/app/output swipenest
```
## ⚙️ Configuration
Edit `Config.txt` to customize:
- INPUT_DIR: Input directory path
- OUTPUT_DIR: Output directory path
- AUDIO_FORMAT: Audio format (wav/mp3)
- MODEL: Whisper model (tiny/base/small/medium/large)
- LANGUAGE: Language code (en, es, fr, etc.) or 'auto' for automatic detection
