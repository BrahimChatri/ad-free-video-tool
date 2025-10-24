Got it 👍 — since you removed the **download** and **Instagram** functions from your tool, here’s your cleaned-up **README** version that reflects only the YouTube “watch without ads” feature.

---

# Watch Without Ads Tool

This is a simple web application built with Flask, allowing users to input **YouTube video URLs** to watch videos without ads.
The app uses `yt-dlp` to fetch and stream the video content directly — providing a smooth, ad-free experience.

## Features

* **Watch Videos Without Ads**: Users can input valid YouTube video URLs to watch videos without interruptions from ads.
* **Responsive Design**: Works seamlessly on both desktop and mobile devices.

## Requirements

To run the application, you’ll need the following installed:

* Python 3.12
* Flask
* yt-dlp

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BrahimChatri/ad-free-video-tool.git
cd watch-without-ads
```

### 2. Install dependencies

It’s recommended to create a virtual environment first.

```bash
python -m venv venv
venv\Scripts\activate  # if you want to use a virtual environment
pip install -r requirements.txt
```

### 3. Running the App

Run the Flask development server by executing:

```bash
python api/app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000/
```

## How It Works

1. **Input URL**: The user enters a valid YouTube video URL.
2. **Watch Without Ads**: The application streams the video directly using `yt-dlp`, bypassing all ads and interruptions.

## Folder Structure

```
/ad-free-video-tool
    /api 
        /app.py           # The main Flask application
    /static
        /styles.css       # Custom styles
        /playlist.css     # Styles for the /playlist page
        /background.svg   # Background image 
        /favicon.ico      # Favicon 
        /github-logo.svg  # GitHub logo for the footer
    /templates
        index.html        # Main HTML page for video streaming
        playlist.html     # HTML page for the /playlist route
    requirements.txt      # Python dependencies
    README.md             # This file
    LICENSE               # MIT License
    vercel.json           # Configuration for Vercel deployment
```

## Troubleshooting

### Video URL Not Valid

If the video URL is not recognized, ensure it is a valid **YouTube** link.
Currently, the app only supports YouTube videos.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
