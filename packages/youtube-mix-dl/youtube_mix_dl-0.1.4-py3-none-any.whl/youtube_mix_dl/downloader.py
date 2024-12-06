from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import yt_dlp
from typing import List, Optional, Callable, Union, Dict, Any
from urllib.parse import parse_qs, urlparse
from .utils import clean_youtube_url

class YouTubeDownloader:
    """A class to download videos from YouTube, playlists, and YouTube Mix"""
    
    def __init__(self, output_path: str = "downloads", progress_callback: Optional[Callable] = None):
        """
        Initialize the YouTube Downloader
        
        Args:
            output_path (str): Directory to save downloaded videos
            progress_callback (callable): Optional callback for progress updates
        """
        self.output_path = output_path
        self.progress_callback = progress_callback
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Chrome webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _extract_playlist_id(self, url: str) -> Optional[str]:
        """Extract playlist ID from URL"""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        return query_params.get('list', [None])[0]
    
    def get_playlist_videos(self, playlist_url: str, num_videos: Optional[int] = None) -> List[str]:
        """
        Extract video URLs from a YouTube playlist
        
        Args:
            playlist_url (str): URL of the YouTube playlist
            num_videos (int, optional): Number of videos to extract, None for all
            
        Returns:
            List[str]: List of video URLs
        """
        driver = self._setup_driver()
        video_urls = []
        playlist_id = self._extract_playlist_id(playlist_url)
        
        if not playlist_id:
            if self.progress_callback:
                self.progress_callback("Invalid playlist URL")
            return []
        
        try:
            if self.progress_callback:
                self.progress_callback("Loading playlist page...")
            driver.get(playlist_url)
            time.sleep(3)
            
            last_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                
                items = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
                
                for item in items:
                    href = item.get_attribute("href")
                    if href and "watch?v=" in href:
                        clean_url = clean_youtube_url(href)
                        if clean_url not in video_urls:
                            video_urls.append(clean_url)
                            if self.progress_callback:
                                self.progress_callback(f"Found {len(video_urls)} videos...")
                
                if num_videos and len(video_urls) >= num_videos:
                    break
                    
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                    
        finally:
            driver.quit()
        
        return video_urls[:num_videos] if num_videos else video_urls
    
    def get_mix_videos(self, mix_url: str, num_videos: int = 25) -> List[str]:
        """
        Extract video URLs from YouTube Mix
        
        Args:
            mix_url (str): URL of the YouTube Mix
            num_videos (int): Number of videos to extract
            
        Returns:
            List[str]: List of video URLs
        """
        driver = self._setup_driver()
        video_urls = []
        
        try:
            if self.progress_callback:
                self.progress_callback("Loading mix playlist page...")
            driver.get(mix_url)
            time.sleep(3)
            
            while len(video_urls) < num_videos:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                
                items = driver.find_elements(By.CSS_SELECTOR, 
                    "a.yt-simple-endpoint.style-scope.ytd-playlist-panel-video-renderer")
                
                for item in items:
                    href = item.get_attribute("href")
                    if href and "watch?v=" in href:
                        clean_url = clean_youtube_url(href)
                        if clean_url not in video_urls:
                            video_urls.append(clean_url)
                
                video_urls = list(dict.fromkeys(video_urls))
                if self.progress_callback:
                    self.progress_callback(f"Found {len(video_urls)} videos...")
                
                if len(video_urls) >= num_videos:
                    break
                    
        finally:
            driver.quit()
        
        return video_urls[:num_videos]

    def download_video(self, url: str, format_options: Optional[Dict[str, Any]] = None) -> bool:
        """
        Download a single video with custom format options
        
        Args:
            url (str): Video URL to download
            format_options (Dict[str, Any]): Optional custom format options for yt-dlp
            
        Returns:
            bool: True if download was successful
        """
        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'ignoreerrors': True,
                'no_warnings': False,
                'quiet': False,
                'progress': True,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
            
            if format_options:
                ydl_opts.update(format_options)
            
            if self.progress_callback:
                ydl_opts['progress_hooks'] = [
                    lambda d: self.progress_callback(
                        f"Downloading: {d.get('_percent_str', '0%')} of {d.get('_total_bytes_str', 'Unknown')}"
                    ) if d['status'] == 'downloading' else None
                ]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if info:
                    if self.progress_callback:
                        self.progress_callback(f"Successfully downloaded: {info.get('title', 'Unknown title')}")
                    return True
                return False

        except Exception as e:
            if self.progress_callback:
                self.progress_callback(f"Error downloading video: {str(e)}")
            return False
    
    def download_mix(self, mix_url: str, num_videos: int = 25) -> int:
        """
        Download videos from a YouTube Mix playlist
        
        Args:
            mix_url (str): URL of the YouTube Mix
            num_videos (int): Number of videos to download
            
        Returns:
            int: Number of successfully downloaded videos
        """
        if self.progress_callback:
            self.progress_callback("Starting YouTube Mix downloader...")
            
        video_urls = self.get_mix_videos(mix_url, num_videos)
        return self._download_multiple_videos(video_urls)

    def download_playlist(self, playlist_url: str, num_videos: Optional[int] = None) -> int:
        """
        Download videos from a YouTube playlist
        
        Args:
            playlist_url (str): URL of the YouTube playlist
            num_videos (int, optional): Number of videos to download, None for all
            
        Returns:
            int: Number of successfully downloaded videos
        """
        if self.progress_callback:
            self.progress_callback("Starting YouTube playlist downloader...")
            
        video_urls = self.get_playlist_videos(playlist_url, num_videos)
        return self._download_multiple_videos(video_urls)

    def _download_multiple_videos(self, video_urls: List[str]) -> int:
        """Helper method to download multiple videos"""
        successful_downloads = 0
        
        for index, video_url in enumerate(video_urls, 1):
            if self.progress_callback:
                self.progress_callback(f"[{index}/{len(video_urls)}] Processing video...")
            if self.download_video(video_url):
                successful_downloads += 1
            time.sleep(1)
        
        if self.progress_callback:
            self.progress_callback(f"Download complete! Successfully downloaded {successful_downloads} videos.")
            
        return successful_downloads

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a video without downloading it
        
        Args:
            url (str): Video URL
            
        Returns:
            Optional[Dict[str, Any]]: Video information or None if failed
        """
        try:
            clean_url = clean_youtube_url(url)
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(clean_url, download=False)
                
        except Exception as e:
            if self.progress_callback:
                self.progress_callback(f"Error getting video info: {str(e)}")
            return None