# Load Lib
import os
import json
import logging
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import yt_dlp

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up YouTube API client
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_channel_id(channel_url):
    try:
        handle = channel_url.split('@')[-1]
        response = youtube.search().list(
            part='snippet',
            q=handle,
            type='channel',
            maxResults=1
        ).execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['channelId']
        else:
            logger.error(f"No channel found for URL: {channel_url}")
            return None
    except HttpError as e:
        error_content = json.loads(e.content)
        error_message = error_content['error']['message'] if 'error' in error_content else str(e)
        logger.error(f"HTTP Error {e.resp.status} occurred: {error_message}")
        return None

def get_channel_videos(channel_id):
    videos = []
    next_page_token = None

    while True:
        try:
            response = youtube.search().list(
                channelId=channel_id,
                type='video',
                part='id,snippet',
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                videos.append({
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description']
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        except HttpError as e:
            logger.error(f"An error occurred: {e}")
            break

    return videos

def download_video(video_url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'verbose': True,
        'logger': logger,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=True)
            return True, info['title']
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return False, None

def main():
    channel_url = input("Enter the YouTube channel URL (e.g., https://www.youtube.com/@TheStandardPodcast): ")
    
    channel_id = get_channel_id(channel_url)
    if not channel_id:
        logger.error("Could not retrieve channel ID. Exiting.")
        return

    videos = get_channel_videos(channel_id)
    logger.info(f"Found {len(videos)} videos in the channel.")

    base_output_folder = 'downloads'
    channel_folder = sanitize_filename(channel_url.split('@')[-1])
    output_folder = os.path.join(base_output_folder, channel_folder)
    os.makedirs(output_folder, exist_ok=True)

    video_data = {}
    for index, video in enumerate(videos, 1):
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        logger.info(f"Downloading video {index}/{len(videos)}: {video['title']}")
        
        success, title = download_video(video_url, output_folder)
        
        if success:
            logger.info(f"Successfully downloaded: {title}")
            
            # Save description
            description_filename = sanitize_filename(f"{title}_description.txt")
            description_path = os.path.join(output_folder, description_filename)
            with open(description_path, 'w', encoding='utf-8') as f:
                f.write(video['description'])
            logger.info(f"Saved video description to: {description_filename}")

            video_filename = sanitize_filename(f"{title}.mp4")
            video_data[video_filename] = video['description']
        else:
            logger.error(f"Failed to download video: {video['id']}")

    # Save JSON file with all video information
    json_path = os.path.join(output_folder, 'video_info.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(video_data, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved video information to: video_info.json")

    logger.info("Channel download completed.")

if __name__ == "__main__":
    main()
