import os
import shutil
import yt_dlp

def download_youtube_video(url, output_path="downloads", download_type="best", quality="best"):
    """
    Download a YouTube video or audio to the specified output path.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video
        download_type (str): 'video', 'audio', or 'best'
        quality (str): 'best', 'high', 'medium', 'low' (for video only)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    has_ffmpeg = bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))

    # Set format based on download type
    if download_type == "audio":
        # Prefer m4a/opus so it plays without conversion; convert to mp3 if ffmpeg is available
        format_str = 'bestaudio[ext=m4a]/bestaudio/best'
        postprocessor = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        } if has_ffmpeg else None
    elif download_type == "video":
        if quality == "best":
            format_str = 'bestvideo+bestaudio/best'
        elif quality == "high":
            format_str = 'bestvideo[height<=1080]+bestaudio/best'
        elif quality == "medium":
            format_str = 'bestvideo[height<=720]+bestaudio/best'
        elif quality == "low":
            format_str = 'bestvideo[height<=480]+bestaudio/best'
        else:
            format_str = 'bestvideo+bestaudio/best'

        # If ffmpeg is missing, fall back to progressive mp4 to avoid merge failures
        if not has_ffmpeg:
            format_str = 'bestvideo[ext=mp4][height<=1080][protocol!="dash"]/best[ext=mp4]/best'
        postprocessor = {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'} if has_ffmpeg else None
    else:  # best
        format_str = 'bestvideo+bestaudio/best'
        if not has_ffmpeg:
            format_str = 'bestvideo[ext=mp4][protocol!="dash"]/best[ext=mp4]/best'
        postprocessor = {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'} if has_ffmpeg else None
    
    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s').replace('\\', '/'),
        'quiet': False,
        'no_warnings': False,
        'postprocessors': [postprocessor] if postprocessor else [],
        'prefer_ffmpeg': has_ffmpeg,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # pyright: ignore[reportArgumentType]
            print(f"Downloading: {url}")
            print(f"Type: {download_type.upper()}" + (f" | Quality: {quality.upper()}" if download_type == "video" else ""))
            info = ydl.extract_info(url, download=True)
            print(f"✓ Downloaded: {info.get('title')}")
    except Exception as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
            print(f"\n✗ FFmpeg Error: {e}")
            print("\nFFmpeg is required for audio conversion.")
            print("To install FFmpeg:")
            print("  • Download from: https://ffmpeg.org/download.html")
            print("  • Or use: choco install ffmpeg (requires admin)")
            print("  • Or use: winget install ffmpeg")
            print("\nAlternatively, download video as-is without conversion.")
        else:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    # Example usage
    print("=" * 50)
    print("YouTube Downloader")
    print("=" * 50)
    
    video_url = input("Enter YouTube URL: ").strip()
    
    print("\nDownload Options:")
    print("1. Audio Only (MP3)")
    print("2. Video (Best Quality)")
    print("3. Video with Custom Quality")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        download_youtube_video(video_url, download_type="audio")
    elif choice == "2":
        download_youtube_video(video_url, download_type="video", quality="best")
    elif choice == "3":
        print("\nQuality Options:")
        print("1. Best (up to 4K)")
        print("2. High (up to 1080p)")
        print("3. Medium (up to 720p)")
        print("4. Low (up to 480p)")
        
        quality_choice = input("\nSelect quality (1-4): ").strip()
        quality_map = {"1": "best", "2": "high", "3": "medium", "4": "low"}
        quality = quality_map.get(quality_choice, "best")
        download_youtube_video(video_url, download_type="video", quality=quality)
    else:
        print("Invalid option. Using best quality video download.")
        download_youtube_video(video_url)