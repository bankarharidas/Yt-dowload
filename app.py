import os
import shutil
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
from playlist import download_youtube_video

app = Flask(__name__)

# Configure upload folder
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    has_ffmpeg = bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))
    return render_template('index.html', has_ffmpeg=has_ffmpeg)

@app.route('/download', methods=['POST'])
def download():
    """Handle download requests."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        download_type = data.get('type', 'best')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'success': False, 'error': 'Please provide a valid YouTube URL'}), 400
        
        # Download the video
        download_youtube_video(url, output_path=DOWNLOAD_FOLDER, download_type=download_type, quality=quality)
        
        return jsonify({'success': True, 'message': 'Download completed successfully!'})
    
    except Exception as e:
        error_msg = str(e)
        if "ffmpeg" in error_msg.lower() or "ffprobe" in error_msg.lower():
            return jsonify({
                'success': False, 
                'error': 'FFmpeg is required but not installed. Please install FFmpeg to continue.',
                'is_ffmpeg_error': True
            }), 500
        return jsonify({'success': False, 'error': f'Download failed: {error_msg}'}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("YouTube Downloader Web Interface")
    print("=" * 60)
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
