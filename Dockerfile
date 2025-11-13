FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install CPU-only Torch first (keeps versions compatible), then other deps
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root safety (optional)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["bash", "entrypoint.sh"]
