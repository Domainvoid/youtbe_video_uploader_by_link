import instaloader
from pytube import YouTube
import os
import functions
from youtube_uploader import uploding
def download_youtube_video(url):
    try:
        direc = "shorts"
        # Create directory if it doesn't exist
        if not os.path.exists(direc):
            os.makedirs(direc)
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=direc)
        #print(f"Video downloaded from YouTube: {yt.title}")
        functions.yt_title()
    except Exception as e:
        pass
        #print(f"Error downloading YouTube video: {e}")

def download_instagram_reel(url):
    try:
        L = instaloader.Instaloader(dirname_pattern="reels")
        L.download_videos = True
        L.download_pictures = False
        L.download_video_thumbnails = False
        L.save_metadata = False
        L.download_comments = False

        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=post.owner_username)
        print(f"Instagram reel downloaded: {shortcode}")
        functions.insta_title()
    except Exception as e:
        pass
        #print(f"Error downloading Instagram reel: {e}")

def urlinput(video_url):
    if "instagram" in video_url:
        download_instagram_reel(video_url)
        uploding()
        print("block done!")
    elif "youtube" in video_url:
        download_youtube_video(video_url)
        uploding()
    else:
        pass
        #print("URL not recognized. Please provide a valid Instagram or YouTube URL.")

# Example Usage
# urlinput("your_instagram_or_youtube_url_here")
