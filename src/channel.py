
import requests

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала и API ключом."""
        self.channel_id = channel_id
        self.api_key = api_key

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        response = requests.get(url)
        data = response.json()

        if 'items' in data and data['items']:
            channel_data = data['items'][0]
            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            print("Title:", snippet['title'])
            print("Description:", snippet['description'])
            print("View Count:", statistics['viewCount'])
            print("Subscriber Count:", statistics['subscriberCount'])
            print("Video Count:", statistics['videoCount'])
        else:
            print("Канал с указанным идентификатором не найден или отсутствует доступ к API")

if __name__ == '__main__':

    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A', api_key)
    moscowpython.print_info()
