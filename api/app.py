from flask import Flask, render_template, request, send_file, Response
import yt_dlp
import re
from pathlib import Path

# Update template directory for Vercel
app = Flask(__name__, static_folder='../static')
template_dir = Path(__file__).parent.parent / "templates"
app.template_folder = str(template_dir)

# Your existing regex patterns
YOUTUBE_SHORTS_REGEX = r'https:\/\/youtube\.com\/shorts\/([a-zA-Z0-9_-]+)\?'
YOUTUBE_REGEX = r'(?:https?:\/\/(?:www\.)?youtube\.com\/(?:[^\/]+\/[^\?]+|(?:v|e(?:mbed)?)\/([^\/\?\&]+)|.*v=([^\/\?\&]+))|youtu\.be\/([^\/\?\&]+))'
INSTAGRAM_REGEX = r'https:\/\/www\.instagram\.com\/reel\/([a-zA-Z0-9_-]+)\/'

@app.route('/', methods=['GET', 'POST'])
def home():
    video_id = None
    download_link = None
    video_type = None

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
            return "Invalid URL. Please enter a valid YouTube or Instagram URL."

    return render_template('index.html', video_id=video_id, download_link=download_link, video_type=video_type)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url', '')
    if not url:
        return "No URL provided", 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']
            video_title = info_dict.get('title', 'video').replace(" ", "_")
            video_ext = info_dict.get('ext', 'mp4')

            def generate():
                with yt_dlp.YoutubeDL() as inner_ydl:
                    response = inner_ydl.urlopen(video_url)
                    chunk_size = 1024 * 1024
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk

            return Response(
                generate(),
                mimetype=f"video/{video_ext}",
                headers={
                    'Content-Disposition': f'attachment; filename="{video_title}.{video_ext}"'
                }
            )
    except Exception as e:
        return f"Error: {str(e)}", 500

# For static files
@app.route('/<path:path>')
def static_proxy(path):
    try:
        return app.send_static_file(path)
    except:
        return app.send_static_file('index.html')

# # For development only
# if __name__ == '__main__':
#     app.run(debug=True)