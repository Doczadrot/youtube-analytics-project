from googleapiclient.discovery import build
import json

class Channel:
    def __init__(self, channel_id: str, api_key: str) -> None:
        self.channel_id = channel_id
        self.api_key = api_key

    def get_channel_info(self) -> dict:
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        try:
            response = request.execute()
            channel_data = response.get('items', [])
            if channel_data:
                channel = channel_data[0]
                snippet = channel.get('snippet', {})
                statistics = channel.get('statistics', {})
                channel_info = {
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'subscriber_count': statistics.get('subscriberCount', ''),
                    'video_count': statistics.get('videoCount', ''),
                    'view_count': statistics.get('viewCount', ''),
                    'url': f"https://www.youtube.com/channel/{self.channel_id}"
                }
                channel_info = {k: v for k, v in channel_info.items() if v}
                return channel_info
            else:
                return {}
        except Exception as e:
            print(f"Ошибка при получении информации о канале: {e}")
            return {}

    def to_json(self, filename: str) -> None:
        channel_info = self.get_channel_info()
        if channel_info:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(channel_info, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'
    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
    moscowpython = Channel(channel_id, api_key)
    channel_info = moscowpython.get_channel_info()

    for key, value in channel_info.items():
        print(f"{key}: {value}")

    try:
        moscowpython.channel_id = 'Новое название'
    except AttributeError as e:
        print(f"Ошибка при изменении channel_id: {e}")

    moscowpython.to_json('moscowpython.json')