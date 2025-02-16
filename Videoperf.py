import streamlit as st
import requests
import pandas as pd

# Streamlit app title
st.title('YouTube Video Performance Comparison Tool')

# Inputs for API Key and Channel ID
api_key = st.text_input('AIzaSyD1yebvf2bpu0A9E6v4w5MhRzGGmaSG7Io')
channel_id = st.text_input('https://www.youtube.com/@CatsCorneryt1')

# Function to fetch videos
def get_videos(api_key, channel_id):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 50,
        'order': 'date',
        'type': 'video',
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    videos = response.json().get('items', [])

    video_ids = [video['id']['videoId'] for video in videos]
    return video_ids, videos

# Function to fetch video statistics
def get_video_stats(api_key, video_ids):
    stats_url = "https://www.googleapis.com/youtube/v3/videos"
    stats_params = {
        'part': 'snippet,contentDetails,statistics',
        'id': ','.join(video_ids),
        'key': api_key
    }
    response = requests.get(stats_url, params=stats_params)
    return response.json().get('items', [])

# Display video statistics
if st.button('Fetch Video Statistics'):
    if api_key and channel_id:
        video_ids, videos = get_videos(api_key, channel_id)
        if video_ids:
            video_stats = get_video_stats(api_key, video_ids)
            data = []
            for video, stats in zip(videos, video_stats):
                video_info = {
                    'Title': video['snippet']['title'],
                    'Published At': video['snippet']['publishedAt'],
                    'Views': stats['statistics'].get('viewCount', 0),
                    'Likes': stats['statistics'].get('likeCount', 0),
                    'Comments': stats['statistics'].get('commentCount', 0),
                    'Video URL': f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                }
                data.append(video_info)
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.error("No videos found. Check your API Key and Channel ID.")
    else:
        st.error("Please enter both an API Key and a Channel ID.")

