
# Watch & Download Tool (Without Ads)

This is a simple web application built with Flask, allowing users to input YouTube or Instagram URLs to watch videos without ads and download them directly to their devices. The app uses `yt-dlp` to download the videos and provides an ad-free viewing experience.

## Features

- **Watch Videos Without Ads**: Users can input valid YouTube or Instagram video URLs to watch the video without interruptions from ads.
- **Download Videos**: Users can download YouTube or Instagram videos directly to their device by clicking the "Download Video" button.
- **Responsive Design**: The application is fully responsive and works well on both desktop and mobile devices.

## Requirements

To run the application, you will need to have the following installed:

- Python 3.7+ 
- Flask
- yt-dlp

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BrahimChatri/ad-free-video-tool.git
cd watch-without-ads
```

### 2. Install dependencies

It is recommended to create a virtual environment first.

```bash
python -m venv venv
venv\Scripts\activate # if you wanna use vertual envirment 
pip install -r requirements.txt
```


### 3. Running the App

Run the Flask development server by executing:

```bash
python app.py
```

You should now be able to access the app by visiting `http://127.0.0.1:5000/` in your browser.

## How It Works

1. **Input URL**: The user enters a valid YouTube or Instagram video URL.
2. **Watch Without Ads**: The application streams the video in a way that avoids any interruptions from ads.
3. **Download**: The user can click the "Download Video" button to start the video download to their device.

The backend uses `yt-dlp`, a command-line program to download videos from YouTube and other sites, to fetch and serve the video file directly to the user's device.

## Folder Structure

```
/ad-free-video-tool
    /api 
        /app.py           # The main Python file running the Flask app
    /static
        /styles.css       # Custom styles for the application
        /playlist.css     # Custom styles for  /playlist \
        /backgroud.svg    # Background image 
        /favicon.ico      # Favicon 
        /github-logo.svg  # Github logo for the footer
    /templates
        index.html        # Main HTML page with video streaming and download functionality
        playlist.html     # Main HTML for /playlist page
    requirements.txt      # List of Python dependencies
    README.md             # This file
    LICENSE               # MIT License file 
    vercel.json           # Configuration file for vercel deployments
```

## Troubleshooting

### Slow Downloads

If the video downloads are slow, it might be due to network conditions or the server's limitations. Ensure that your internet connection is stable, and consider configuring the download options to fetch the best format.

### Video URL Not Valid

If the video URL is not recognized, ensure that it is a valid YouTube or Instagram URL. The app currently only supports these two platforms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

