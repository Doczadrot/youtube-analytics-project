import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode

class Video:
    def __init__(self, video_id, api_key):
        self.video_id = video_id
        self.title = None
        self.like_count = None
        self.duration = None
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,statistics,contentDetails"
            response = requests.get(url)
            response.raise_for_status()
            video_data = response.json()["items"][0]
            self.title = video_data["snippet"]["title"]
            self.like_count = video_data["statistics"].get("likeCount", 0)
            duration = video_data["contentDetails"]["duration"]
            self.duration = parse_duration(duration)
        except (IndexError, KeyError, requests.exceptions.RequestException):
            pass

def parse_duration(duration_str):
    duration_components = duration_str.split("PT")[1].split("M")
    hours = int(duration_components[0]) if duration_components[0] else 0
    minutes = int(duration_components[1].split("S")[0]) if len(duration_components) > 1 and duration_components[1] else 0
    seconds = int(duration_components[-1][:-1]) if len(duration_components) > 1 and duration_components[-1][-1] == "S" else 0
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

if __name__ == '__main__':
    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
    broken_video = Video('broken_video_id', api_key)
    assert broken_video.video_id == 'broken_video_id'
    assert broken_video.title is None
    assert broken_video.like_count is None
    assert broken_video.duration is None