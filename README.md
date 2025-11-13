Automatically extract audio and generate subtitles from any video using OpenAI’s Whisper (via Faster-Whisper).

Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate

install dependencies : pip install -r requirements.txt

Run the app : python -m src.main

Build Image : docker build -t swipenest-subtitles .

Run Container : docker run -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" swipenest-subtitles


# 🎬 Swipenest Subtitles Generator

Automatically generate subtitles for any video using **OpenAI Whisper** and **FFmpeg**.

---

## 🚀 Features
- Accepts any video format (MP4, MKV, AVI, MOV, etc.)
- Extracts audio automatically using FFmpeg
- Generates accurate subtitles using Whisper
- Exports `.srt` subtitle files
- Works in both local and Docker environments

- Tanmay Ghanwat