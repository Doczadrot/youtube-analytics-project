import os
from googleapiclient.discovery import build
import datetime

class PlayList:
    """Класс для работы с плейлистами YouTube."""

    __API_KEY = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"  # <<--- ЗАМЕНИТЕ НА ВАШ КЛЮЧ

    def __init__(self, playlist_id: str) -> None:
        """Инициализируем ID плейлиста и загружаем данные из API."""
        self.__playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        """Загружает данные о плейлисте и видео из YouTube API."""
        youtube = self.get_service()

        # Получение информации о плейлисте
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=self.__playlist_id
        ).execute()
        playlist_item = playlist_response['items'][0]
        self.title = playlist_item['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

        # Получение списка видео в плейлисте
        self.videos = []
        nextPageToken = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=self.__playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()
            for item in playlist_items_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video = Video(video_id)
                self.videos.append(video)
            nextPageToken = playlist_items_response.get('nextPageToken')
            if not nextPageToken:
                break

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект сервиса YouTube API."""
        return build('youtube', 'v3', developerKey=cls.__API_KEY)

    @property
    def total_duration(self):
        """Возвращает суммарную продолжительность всех видео в плейлисте."""
        total_seconds = sum(video.duration.total_seconds() for video in self.videos)
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        """Возвращает URL самого популярного видео в плейлисте."""
        best_video = max(self.videos, key=lambda video: video.like_count)
        return f"https://youtu.be/{best_video.video_id}"

class Video:
    """Класс для работы с видео YouTube."""

    def __init__(self, video_id: str) -> None:
        """Инициализирует ID видео и загружает данные из API."""
        self.video_id = video_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        """Загружает данные о видео из YouTube API."""
        youtube = PlayList.get_service()
        video_response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=self.video_id
        ).execute()
        video_item = video_response['items'][0]
        self.title = video_item['snippet']['title']
        self.like_count = int(video_item['statistics']['likeCount'])
        self.duration = parse_duration(video_item['contentDetails']['duration'])

def parse_duration(duration_str):
    """Функция для преобразования строки продолжительности из API в объект datetime.timedelta"""
    if not duration_str:
        return datetime.timedelta()

    duration_components = duration_str.split("PT")[1].split("M")
    hours = int(duration_components[0]) if len(duration_components) > 0 and duration_components[0] else 0
    minutes = int(duration_components[1][:-1]) if len(duration_components) > 1 and duration_components[1][:-1] else 0

    # Проверка длины строки перед доступом к последнему символу
    seconds = int(duration_components[1][-1]) if len(duration_components) > 1 and len(duration_components[1]) > 1 and duration_components[1][-1].isdigit() else 0

    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)