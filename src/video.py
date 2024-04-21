# src/video.py

import requests

class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.get_video_info()

    def get_video_info(self):
        api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
        url = f"https://www.googleapis.com/youtube/v3/videos?id={self.video_id}&key={api_key}&part=snippet,statistics"
        response = requests.get(url).json()

        if response["items"]:
            video_data = response["items"][0]
            self.title = video_data["snippet"]["title"]
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = video_data["statistics"]["viewCount"]
            self.like_count = video_data["statistics"]["likeCount"]
        else:
            raise ValueError(f"Видео с ID {self.video_id} не найдено.")

    def __str__(self):
        return self.title

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title} (Плейлист {self.playlist_id})"