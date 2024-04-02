from googleapiclient.discovery import build
import json

class Channel:
    """
    Класс для работы с информацией о YouTube канале.
    """

    def __init__(self, channel_id: str, api_key: str) -> None:
        """
        Инициализирует экземпляр класса Channel.

        :param channel_id: Идентификатор YouTube канала.
        :param api_key: Ключ API YouTube.
        """
        self.channel_id = channel_id
        self.api_key = api_key

    def get_channel_info(self) -> dict:
        """
        Получает информацию о канале с использованием YouTube API.
        """
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
                return {
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'subscriber_count': statistics.get('subscriberCount', ''),
                    'video_count': statistics.get('videoCount', ''),
                    'view_count': statistics.get('viewCount', ''),
                    'url': f"https://www.youtube.com/channel/{self.channel_id}"
                }
            else:
                print("Ответ YouTube API не содержит информации о канале")
                return {}
        except Exception as e:
            print(f"Ошибка при получении информации о канале: {e}")
            return {}

    def to_json(self, filename: str) -> None:
        """
        Сохраняет информацию о канале в файл JSON.

        :param filename: Имя файла для сохранения информации.
        """
        channel_info = self.get_channel_info()
        if channel_info:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(channel_info, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # Идентификатор канала, информацию о котором мы хотим получить
    channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'

    # Ключ API YouTube
    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"

    # Создаем экземпляр класса Channel для указанного канала с передачей ключа API
    moscowpython = Channel(channel_id, api_key)

    # Получаем информацию о канале с использованием YouTube API
    channel_info = moscowpython.get_channel_info()

    # Получаем значения атрибутов и выводим их
    print(f"Название канала: {channel_info['title']}")
    print(f"Количество видео: {channel_info['video_count']}")
    print(f"Ссылка на канал: {channel_info['url']}")

    # Попытка изменить channel_id (должно вызвать ошибку, так как это только для чтения)
    try:
        moscowpython.channel_id = 'Новое название'
    except AttributeError as e:
        print(f"Ошибка при изменении channel_id: {e}")

    # Сохраняем информацию о канале в файл JSON
    moscowpython.to_json('moscowpython.json')
