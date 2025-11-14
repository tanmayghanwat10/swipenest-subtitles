<<<<<<< Updated upstream

=======
### YouTube Videos
Create `.url` files in the `input/` directory with YouTube URLs (one per file) and run:
```bash
python -m src.main_youtube
```
=======
>>>>>>> Stashed changes
Automatically extract audio and generate subtitles from any video using OpenAI’s Whisper (via Faster-Whisper).

Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate

install dependencies : pip install -r requirements.txt

Run the app for local videos: python -m src.main_local
Run the app for YouTube videos: python -m src.main_youtube

Build Image : docker build -t swipenest-subtitles .

Run Container : docker run -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" swipenest-subtitles


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
=======
<<<<<<< Updated upstream
=======
# Swipenest Subtitles Generator

Automatically generate subtitles for any video using **OpenAI Whisper** and **FFmpeg**.

---

## 🚀 Features
- Accepts any video format (MP4, MKV, AVI, MOV, etc.)
- Extracts audio automatically using FFmpeg
- Generates accurate subtitles using Whisper (supports multiple languages with auto-detection)
- Exports `.srt` subtitle files
- Works in both local and Docker environments
- Supports YouTube video URLs via .url files
- Tanmay Ghanwat

---

## 📋 Requirements
- Python 3.8+
- FFmpeg
- yt-dlp (for YouTube support)

---

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

---

## 🎯 Usage

### For Local Videos
Place your video files in the `input/` directory and run:
```bash
python -m src.main
```
Select "local" when prompted.

### For YouTube Videos
Create a `.url` file in the `input/` directory containing the YouTube URL (one per file), then run:
```bash
python -m src.main
```
Select "youtube" when prompted.

### Separate Scripts
- Local videos: `python -m src.main_local`
- YouTube URLs: `python -m src.main_youtube`

---

## 🐳 Docker Usage

Build Image:
```bash
docker build -t swipenest-subtitles .
```

Run Container:
```bash
docker run -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" swipenest-subtitles
```

---

## ⚙️ Configuration
Edit `Config.txt` to customize:
- INPUT_DIR: Input directory path
- OUTPUT_DIR: Output directory path
- AUDIO_FORMAT: Audio format (wav/mp3)
- MODEL: Whisper model (tiny/base/small/medium/large)
- LANGUAGE: Language code (en, es, fr, etc.) or 'auto' for automatic detection
>>>>>>> Stashed changes
