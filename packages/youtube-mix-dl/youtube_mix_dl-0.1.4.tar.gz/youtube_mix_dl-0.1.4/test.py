#from youtube_mix_dl import YoutubeMixDownloader
#
## Initialize the downloader
#downloader = YoutubeMixDownloader(output_path="downloads")
#
## Define a progress callback (optional)
#def progress_callback(message):
#    print(message)
#
## Create downloader with callback
#downloader = YoutubeMixDownloader(
#    output_path="downloads",
#    progress_callback=progress_callback
#)
#
## Download a mix
#mix_url = "https://www.youtube.com/watch?v=Mude7cCSs9s&list=RDMude7cCSs9s&start_radio=1"
#num_videos = 25
#successful_downloads = downloader.download_mix(mix_url, num_videos)
#
#print(f"Downloaded {successful_downloads} videos successfully")




#from youtube_mix_dl import YouTubeDownloader
#
## Basic download
#downloader = YouTubeDownloader(output_path="downloads")
#success = downloader.download_video("https://www.youtube.com/watch?v=fcJwqnj6_xI")

from youtube_mix_dl import YouTubeDownloader

def progress_callback(message):
    print(message)

# Initialize downloader
downloader = YouTubeDownloader(
    output_path="downloads",
    progress_callback=progress_callback
)



# 4. Download from normal playlist
playlist_url = "https://www.youtube.com/playlist?list=PLPTV0NXA_ZSgsLAr8YCgCwhPIJNNtexWu"
print("\nDownloading from normal playlist...")
playlist_downloads = downloader.download_playlist(playlist_url, num_videos=3)
print(f"Downloaded {playlist_downloads} videos from playlist")