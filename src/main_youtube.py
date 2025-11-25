import sys
from src.main import process_youtube_url

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main_youtube <YouTube_URL>")
        sys.exit(1)
    url = sys.argv[1]
    process_youtube_url(url)

if __name__ == "__main__":
    main()
