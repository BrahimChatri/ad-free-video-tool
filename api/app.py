from flask import Flask, render_template, request, send_file, Response
import yt_dlp
import re, os
from pathlib import Path


# Update template directory for Vercel
app = Flask(__name__, static_folder='../static')
template_dir = Path(__file__).parent.parent / "templates"
app.template_folder = str(template_dir)

# Your existing regex patterns
YOUTUBE_SHORTS_REGEX = r'https:\/\/youtube\.com\/shorts\/([a-zA-Z0-9_-]+)\?'
YOUTUBE_REGEX = r'(?:https?:\/\/(?:www\.)?youtube\.com\/(?:[^\/]+\/[^\?]+|(?:v|e(?:mbed)?)\/([^\/\?\&]+)|.*v=([^\/\?\&]+))|youtu\.be\/([^\/\?\&]+))'
INSTAGRAM_REGEX = r'https:\/\/www\.instagram\.com\/reel\/([a-zA-Z0-9_-]+)\/'

@app.context_processor
def inject_timestamp():
    # Get timestamps for both CSS files
    styles_path = os.path.join(app.static_folder, 'styles.css')
    playlist_path = os.path.join(app.static_folder, 'playlist.css')

    styles_timestamp = str(int(os.path.getmtime(styles_path))) if os.path.exists(styles_path) else ''
    playlist_timestamp = str(int(os.path.getmtime(playlist_path))) if os.path.exists(playlist_path) else ''

    return {'css_timestamp': styles_timestamp, 'playlist_css_timestamp': playlist_timestamp}

@app.route('/', methods=['GET', 'POST'])
def home():
    video_id = None
    download_link = None
    video_type = None
    error = None  # Variable to store error messages

    if request.method == 'POST':
        url = request.form.get('video_url', '')

        match_youtube_shorts = re.search(YOUTUBE_SHORTS_REGEX, url)
        match_youtube = re.search(YOUTUBE_REGEX, url)
        match_instagram = re.search(INSTAGRAM_REGEX, url)

        if match_youtube_shorts:
            video_id = match_youtube_shorts.group(1)
            video_type = 'youtube'
            download_link = url
        elif match_youtube:
            video_id = match_youtube.group(2) or match_youtube.group(3) or match_youtube.group(4)
            video_type = 'youtube'
            download_link = url
        elif match_instagram:
            video_id = match_instagram.group(1)
            video_type = 'instagram'
            download_link = url
        else:
            error = "Invalid URL. Please enter a valid URL."

    return render_template('index.html', video_id=video_id, download_link=download_link, video_type=video_type, error=error)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url', '')
    if not url:
        return render_template('index.html', error="No URL provided"), 400

    try:
        # Options for yt-dlp
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'ratelimit': 1000000,  # in bytes per second
            'outtmpl': '/tmp/%(id)s.%(ext)s',  # Output to a temporary file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info without downloading
            info_dict = ydl.extract_info(url, download=True)  # Download the video
            video_title = info_dict.get('title', 'video').replace(" ", "_")
            video_ext = info_dict.get('ext', 'mp4')
            video_file = f"/tmp/{info_dict['id']}.{video_ext}"

            # After downloading, we can create a temporary file and return it
            def generate():
                with open(video_file, 'rb') as f:
                    chunk = f.read(1024 * 1024)  # Read in 1MB chunks
                    while chunk:
                        yield chunk
                        chunk = f.read(1024 * 1024)

            # Return the file as a response (no large payload)
            return Response(
                generate(),
                mimetype=f"video/{video_ext}",
                headers={
                    'Content-Disposition': f'attachment; filename="{video_title}.{video_ext}"'
                }
            )
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error: {str(e)}"
        return render_template('index.html', error=error_message), 500
# root to watch full playlist    
@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    playlist_id = None
    error = None
    if request.method == 'POST':
        playlist_url = request.form.get('video_url', '').strip()
        if "youtube.com/playlist" in playlist_url and "list=" in playlist_url:
            # Extract playlist ID
            playlist_id = playlist_url.split("list=")[-1].split('&')[0]
        else:
            # Handle invalid playlist URL
            error = "Invalid Playlist URL. Please enter a valid YouTube playlist link."

    return render_template('playlist.html', playlist_id=playlist_id, error=error)

# For static files
@app.route('/<path:path>')
def static_proxy(path):
    try:
        return app.send_static_file(path)
    except:
        return app.send_static_file('index.html')

# For development only
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=True)
