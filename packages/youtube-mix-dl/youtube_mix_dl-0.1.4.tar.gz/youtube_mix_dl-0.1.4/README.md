# YouTube Downloader

A Python library for downloading videos from YouTube and YouTube Mix playlists.

[View on GitHub](https://github.com/benny-png/YOUR_YOUTUBE_MUSIC_MIX_DOWNLOADER)

[![Downloads](https://pepy.tech/badge/youtube-mix-dl)](https://pepy.tech/project/youtube-mix-dl)
[![Downloads](https://pepy.tech/badge/youtube-mix-dl/month)](https://pepy.tech/project/youtube-mix-dl)
[![Downloads](https://pepy.tech/badge/youtube-mix-dl/week)](https://pepy.tech/project/youtube-mix-dl)

## Installation

```bash
pip install youtube-mix-dl==0.1.4
```

### Dependencies
```bash
pip install selenium>=4.0.0 webdriver-manager>=3.8.0 yt-dlp>=2023.0.0
```

### System Requirements

#### FFmpeg Installation
- Windows: `winget install FFmpeg`
- Linux: `sudo apt update && sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

- Google Chrome/Chromium browser
- ChromeDriver (auto-installed by webdriver-manager)

## Usage Examples

### Test Script (test.py)
```python
from youtube_mix_dl import YouTubeDownloader

def progress_callback(message):
    print(message)

# Initialize downloader
downloader = YouTubeDownloader(
    output_path="downloads",
    progress_callback=progress_callback
)

# 1. Download single video
video_url = "https://www.youtube.com/watch?v=Mude7cCSs9s"
print("\nDownloading single video...")
success = downloader.download_video(video_url)
print(f"Single video download {'successful' if success else 'failed'}")

# 2. Download audio only
print("\nDownloading audio only...")
audio_options = {
    'format': 'bestaudio[ext=m4a]',
    'postprocessors': [{'key': 'FFmpegExtractAudio'}]
}
success = downloader.download_video(video_url, audio_options)
print(f"Audio download {'successful' if success else 'failed'}")

# 3. Download from music mix playlist
mix_url = "https://www.youtube.com/watch?v=Mude7cCSs9s&list=RDMude7cCSs9s&start_radio=1"
print("\nDownloading from music mix playlist...")
mix_downloads = downloader.download_mix(mix_url, num_videos=3)
print(f"Downloaded {mix_downloads} videos from mix")

# 4. Download from normal playlist
playlist_url = "https://www.youtube.com/playlist?list=PLPTV0NXA_ZSgsLAr8YCgCwhPIJNNtexWu"
print("\nDownloading from normal playlist...")
playlist_downloads = downloader.download_playlist(playlist_url, num_videos=3)
print(f"Downloaded {playlist_downloads} videos from playlist")

# 5. Get video information
print("\nGetting video information...")
info = downloader.get_video_info(video_url)
if info:
    print(f"Video title: {info.get('title')}")
    print(f"Duration: {info.get('duration')} seconds")
    print(f"View count: {info.get('view_count')}")
```

Run the test script:
```bash
python test.py
```

### Individual Features

#### 1. Single Video Download
```python
from youtube_mix_dl import YouTubeDownloader

downloader = YouTubeDownloader(output_path="downloads")
success = downloader.download_video("https://www.youtube.com/watch?v=Mude7cCSs9s")
```

#### 2. Audio Only Download
```python
options = {
    'format': 'bestaudio[ext=m4a]',
    'postprocessors': [{'key': 'FFmpegExtractAudio'}]
}
success = downloader.download_video("https://www.youtube.com/watch?v=Mude7cCSs9s", options)
```

#### 3. Music Mix Playlist Download
```python
downloader = YouTubeDownloader(
    output_path="downloads",
    progress_callback=lambda msg: print(msg)
)
successful_downloads = downloader.download_mix(
    "https://www.youtube.com/watch?v=Mude7cCSs9s&list=RDMude7cCSs9s&start_radio=1",
    num_videos=5
)
```

#### 4. Normal Playlist Download
```python
successful_downloads = downloader.download_playlist(
    "https://www.youtube.com/playlist?list=PLPTV0NXA_ZSgsLAr8YCgCwhPIJNNtexWu",
    num_videos=5
)
```

## Features

- Single video and playlist downloads (music mix and normal playlists)
- Audio-only downloads 
- Progress tracking with callbacks
- High-quality video/audio
- Automatic stream merging
- Error handling
- Video information retrieval

## Troubleshooting

### Common Issues

1. **No Audio**
   - Verify FFmpeg: `ffmpeg -version`
   - Check PATH settings

2. **ChromeDriver Issues**
   - Update Chrome
   - Let webdriver-manager handle installation

3. **Permission Issues**
   - Check output directory permissions
   - Run with appropriate privileges

## Development

```bash
# Setup
git clone https://github.com/benny-png/YOUR_YOUTUBE_MUSIC_MIX_DOWNLOADER.git
cd YOUR_YOUTUBE_MUSIC_MIX_DOWNLOADER
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install build twine pytest black isort mypy
pip install -e .
```

## License

MIT License