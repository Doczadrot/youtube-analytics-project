import requests
import datetime

class Video:
    def __init__(self, video_id, title=None, like_count=None, duration=None):
        self.video_id = video_id
        self.title = title
        self.like_count = like_count
        self.duration = duration

        if not title or not like_count or not duration:
            try:
                self.get_video_info()
            except ValueError as e:
                print(e)

    def get_video_info(self):
        api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
        url = f"https://www.googleapis.com/youtube/v3/videos?id={self.video_id}&key={api_key}&part=snippet,statistics"
        response = requests.get(url).json()

        if response.get("items"):
            video_data = response["items"][0]["snippet"]
            self.title = video_data.get("title")
            self.like_count = response["items"][0]["statistics"].get("likeCount")
            self.duration = self.convert_duration(video_data.get("duration"))
        else:
            raise ValueError(f"Видео с ID {self.video_id} не найдено или данные недоступны.")

    def convert_duration(self, duration):
        # Преобразование продолжительности из формата ISO 8601 в секунды
        pass  # Здесь можно добавить код для преобразования продолжительности, если нужно

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title} (Плейлист {self.playlist_id})"
