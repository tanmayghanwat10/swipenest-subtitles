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

Build Image:
```bash
docker build -t swipenest .
```

Run Container:
```bash
docker run -it --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" swipenest
```
w
## ⚙️ Configuration
Edit `Config.txt` to customize:
- INPUT_DIR: Input directory path
- OUTPUT_DIR: Output directory path
- AUDIO_FORMAT: Audio format (wav/mp3)
- MODEL: Whisper model (tiny/base/small/medium/large)
- LANGUAGE: Language code (en, es, fr, etc.) or 'auto' for automatic detection
