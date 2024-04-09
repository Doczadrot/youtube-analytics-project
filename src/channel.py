# channel.py
from googleapiclient.discovery import build
import json

class Channel:
    def __init__(self, channel_id: str, api_key: str) -> None:
        self._channel_id = channel_id
        self._api_key = api_key
        self.title = None
        self.description = None
        self.channel_url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self._get_channel_info()

    def _get_channel_info(self) -> None:
        youtube = self.get_service(self._api_key)
        request = youtube.channels().list(
            part="snippet,statistics",
            id=self._channel_id
        )
        try:
            response = request.execute()
            channel_data = response.get('items', [])[0]
            if channel_data:
                snippet = channel_data.get('snippet', {})
                statistics = channel_data.get('statistics', {})
                self.title = snippet.get('title', '')
                self.description = snippet.get('description', '')
                self.channel_url = f"https://www.youtube.com/channel/{self._channel_id}"
                self.subscriber_count = statistics.get('subscriberCount', 0)
                self.video_count = statistics.get('videoCount', 0)
                self.view_count = statistics.get('viewCount', 0)
        except Exception as e:
            print(f"Ошибка при получении информации о канале: {e}")

    @classmethod
    def get_service(cls, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        channel_info = {
            'id': self._channel_id,
            'title': self.title,
            'description': self.description,
            'channel_url': self.channel_url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, ensure_ascii=False, indent=4)

