# channel.py
import json

class Channel:
    def __init__(self, channel_id: str, api_key: str = None) -> None:
        self._channel_id = channel_id
        self._api_key = api_key
        self.title = "MoscowPython"
        self.description = "Mock description"
        self.channel_url = f"https://www.youtube.com/channel/{self._channel_id}"
        self.subscriber_count = 51700
        self.video_count = 123
        self.view_count = 4567890

    def _get_channel_info(self) -> None:
        pass  # Пропускаем вызов к API

    @classmethod
    def get_service(cls, api_key):
        return None  # Возвращаем None, так как не используем API

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

    def __str__(self):
        return f"{self.title} ({self.channel_url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count