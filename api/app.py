from flask import Flask, render_template, request
import re
from pathlib import Path


# Update template directory for Vercel
app = Flask(__name__, static_folder='../static')
template_dir = Path(__file__).parent.parent / "templates"
app.template_folder = str(template_dir)

# Your existing regex patterns
YOUTUBE_SHORTS_REGEX = r'https:\/\/youtube\.com\/shorts\/([a-zA-Z0-9_-]+)\?'
YOUTUBE_REGEX = r'(?:https?:\/\/(?:www\.)?youtube\.com\/(?:[^\/]+\/[^\?]+|(?:v|e(?:mbed)?)\/([^\/\?\&]+)|.*v=([^\/\?\&]+))|youtu\.be\/([^\/\?\&]+))'

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
        if match_youtube_shorts:
            video_id = match_youtube_shorts.group(1)
            video_type = 'youtube'
            download_link = url
        elif match_youtube:
            video_id = match_youtube.group(2) or match_youtube.group(3) or match_youtube.group(4)
            video_type = 'youtube'
            download_link = url
        else:
            error = "Invalid URL. Please enter a valid YouTube URL."

    return render_template('index.html', video_id=video_id, download_link=download_link, video_type=video_type, error=error)



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
if __name__ == '__main__':
    app.run(debug=True)
