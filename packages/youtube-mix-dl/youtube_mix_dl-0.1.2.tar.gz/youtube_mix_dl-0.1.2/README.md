# YouTube Downloader

A Python library for downloading videos from YouTube and YouTube Mix playlists.

[View on GitHub](https://github.com/benny-png/YOUR_YOUTUBE_MUSIC_MIX_DOWNLOADER)

[![Downloads](https://pepy.tech/badge/youtube-mix-dl)](https://pepy.tech/project/youtube-mix-dl)
[![Downloads](https://pepy.tech/badge/youtube-mix-dl/month)](https://pepy.tech/project/youtube-mix-dl)
[![Downloads](https://pepy.tech/badge/youtube-mix-dl/week)](https://pepy.tech/project/youtube-mix-dl)

## Installation

```bash
pip install youtube_mix_dl
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

## Usage

### Single Video Download
```python
from youtube_mix_dl import YouTubeDownloader

# Basic download
downloader = YouTubeDownloader(output_path="downloads")
success = downloader.download_video("https://youtube.com/watch?v=...")

# Custom format (e.g., audio only)
options = {
    'format': 'bestaudio[ext=m4a]',
    'postprocessors': [{'key': 'FFmpegExtractAudio'}]
}
success = downloader.download_video("https://youtube.com/watch?v=...", options)

# Get video information
info = downloader.get_video_info("https://youtube.com/watch?v=...")
```

### Mix Playlist Download
```python
# Progress tracking
def progress_callback(message):
    print(message)

downloader = YouTubeDownloader(
    output_path="downloads",
    progress_callback=progress_callback
)

# Download mix
mix_url = "https://www.youtube.com/watch?v=..."
successful_downloads = downloader.download_mix(mix_url, num_videos=25)
```

## Features

- Single video and mix playlist downloads
- Custom format options
- Progress tracking
- High-quality video/audio
- Automatic stream merging
- Error handling

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
cd youtube_mix_dl
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install build twine pytest black isort mypy
pip install -e .

# Tests and formatting
pytest
black . && isort .
```

## License

MIT License