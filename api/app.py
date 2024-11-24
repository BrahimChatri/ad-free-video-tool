from flask import Flask, render_template, request, send_file, Response
import yt_dlp
import re
from pathlib import Path
import requests
import logging
from urllib.parse import urlparse

# Update template directory for Vercel
app = Flask(__name__, static_folder='../static')
template_dir = Path(__file__).parent.parent / "templates"
app.template_folder = str(template_dir)

# Improved regex patterns with named groups
YOUTUBE_SHORTS_REGEX = r'https:\/\/youtube\.com\/shorts\/(?P<video_id>[a-zA-Z0-9_-]+)'
YOUTUBE_REGEX = r'(?:https?:\/\/(?:www\.)?youtube\.com\/(?:[^\/]+\/[^\?]+|(?:v|e(?:mbed)?)\/(?P<vid1>[^\/\?\&]+)|.*v=(?P<vid2>[^\/\?\&]+))|youtu\.be\/(?P<vid3>[^\/\?\&]+))'
INSTAGRAM_REGEX = r'https:\/\/(?:www\.)?instagram\.com\/(?:reel|p)\/(?P<video_id>[a-zA-Z0-9_-]+)'

def get_platform_options(url):
    """Get platform-specific yt-dlp options"""
    domain = urlparse(url).netloc.lower()
    
    base_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': False,
        'no_warnings': False,
        'merge_output_format': 'mp4',
        'prefer_ffmpeg': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    if 'instagram.com' in domain:
        base_opts.update({
            'format': 'best[ext=mp4]/best',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
            }
        })
    elif any(x in domain for x in ['youtube.com', 'youtu.be']):
        base_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'postprocessor_args': [
                '-c:v', 'h264',
                '-c:a', 'aac',
                '-strict', 'experimental'
            ],
        })
    
    return base_opts

@app.route('/', methods=['GET', 'POST'])
def home():
    video_id = None
    download_link = None
    video_type = None
    error = None

    if request.method == 'POST':
        url = request.form.get('video_url', '').strip()

        # Check URL against all patterns
        for pattern, v_type in [
            (YOUTUBE_SHORTS_REGEX, 'youtube'),
            (YOUTUBE_REGEX, 'youtube'),
            (INSTAGRAM_REGEX, 'instagram')
        ]:
            match = re.search(pattern, url)
            if match:
                # Get the first non-None group for video ID
                video_id = next((g for g in match.groups() if g is not None), None)
                video_type = v_type
                download_link = url
                break
        
        if not download_link:
            error = "Invalid URL. Please enter a valid YouTube or Instagram URL."

    return render_template('index.html', video_id=video_id, download_link=download_link, video_type=video_type, error=error)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url', '').strip()
    if not url:
        return render_template('index.html', error="No URL provided"), 400
    
    try:
        # Get platform-specific options
        ydl_opts = get_platform_options(url)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Extracting video info from {url}...")
            info = ydl.extract_info(url, download=False)
            
            if not info:
                raise Exception("Could not extract video information")

            # Get the best video URL
            formats = info.get('formats', [])
            video_url = None
            
            # Try to get the best MP4 format
            for f in formats:
                if f.get('ext') == 'mp4' and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    video_url = f['url']
                    break
            
            # Fallback to any format if no MP4 found
            if not video_url:
                video_url = info.get('url') or formats[-1]['url']

            # Clean the video title
            video_title = info.get('title', 'video')
            video_title = re.sub(r'[^\w\s-]', '', video_title)
            video_title = re.sub(r'[-\s]+', '-', video_title).strip('-')

        def generate():
            with requests.get(video_url, headers=ydl_opts['headers'], stream=True) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    if chunk:
                        yield chunk

        return Response(
            generate(),
            mimetype="video/mp4",
            headers={
                'Content-Disposition': f'attachment; filename="{video_title}.mp4"',
                'Content-Type': 'video/mp4'
            }
        )

    except Exception as e:
        logging.error(f"Download error: {str(e)}", exc_info=True)
        return render_template('index.html', error=f"Error downloading video: {str(e)}"), 500

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    playlist_id = None
    error = None
    if request.method == 'POST':
        playlist_url = request.form.get('video_url', '').strip()
        if "youtube.com/playlist" in playlist_url and "list=" in playlist_url:
            playlist_id = re.search(r'list=([a-zA-Z0-9_-]+)', playlist_url).group(1)
        else:
            error = "Invalid Playlist URL. Please enter a valid YouTube playlist link."

    return render_template('playlist.html', playlist_id=playlist_id, error=error)

# For static files
@app.route('/<path:path>')
def static_proxy(path):
    try:
        return app.send_static_file(path)
    except:
        return app.send_static_file('index.html')

# if __name__ == '__main__':
#     # Configure logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s'
#     )
#     app.run(debug=True)