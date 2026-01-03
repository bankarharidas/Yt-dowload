# YouTube Downloader

A tiny CLI helper in [playlist.py](playlist.py#L1) that downloads YouTube videos or extracts audio using `yt-dlp`, saving files to `downloads/`.

## Requirements
- Python 3.9+
- `yt-dlp` Python package
- (Optional) `ffmpeg` + `ffprobe` on PATH for audio extraction to MP3 and video muxing to MP4

## Setup
1. Clone or copy this folder.
2. In a terminal, create and activate a virtual environment:
   - Windows PowerShell
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -U pip yt-dlp
   ```
4. (Optional) Install FFmpeg if you want MP3 conversion or automatic video muxing:
   - Windows: `winget install ffmpeg` or `choco install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Debian/Ubuntu) or use your distro package manager

## Usage
Run the script and follow the prompts:
```bash
python playlist.py
```
- Paste a YouTube URL when asked.
- Choose:
  - `1` Audio only → saves MP3 when FFmpeg is available (otherwise original audio container).
  - `2` Video (best) → highest available quality; uses FFmpeg to merge streams when present.
  - `3` Video with quality selection:
    - Best (up to 4K)
    - High (up to 1080p)
    - Medium (up to 720p)
    - Low (up to 480p)

Downloads land in `downloads/` (ignored by git). If FFmpeg is missing, the script falls back to formats that do not require merging.

## Notes
- Output template: `downloads/<title>.<ext>`
- The script prints errors and FFmpeg install hints when needed.
- To change the destination or defaults, adjust the `download_youtube_video` call in [playlist.py](playlist.py#L1).
