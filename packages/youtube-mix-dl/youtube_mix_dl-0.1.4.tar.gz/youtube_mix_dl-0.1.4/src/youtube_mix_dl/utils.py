def clean_youtube_url(url: str) -> str:
    """
    Clean YouTube URL by removing playlist parameters
    
    Args:
        url (str): YouTube URL to clean
        
    Returns:
        str: Cleaned URL
    """
    video_id_start = url.find('watch?v=')
    if video_id_start != -1:
        video_id_start += 8
        video_id_end = url.find('&', video_id_start)
        if video_id_end == -1:
            video_id_end = len(url)
        return f"https://www.youtube.com/watch?v={url[video_id_start:video_id_end]}"
    return url