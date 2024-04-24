import datetime
from src.video import Video
from src.playlist import PlayList

if __name__ == '__main__':
    try:
        # Создание экземпляра класса Video для проверки его атрибутов
        broken_video = Video('broken_video_id')
        assert broken_video.title is None
        assert broken_video.like_count is None
        assert broken_video.duration is None
    except ValueError as e:
        print(e)

    # Создание экземпляра класса PlayList для проверки его атрибутов и методов
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw', title="Moscow Python Meetup №81",
                  url="https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw",
                  videos=[
                      Video('cUGyMzWQcGM', title="Video 1", like_count=100, duration=300),  # Продолжительность 5 минут
                      Video('xyz123', title="Video 2", like_count=50, duration=420),        # Продолжительность 7 минут
                      # Добавьте другие видео при необходимости
                  ])

    # Проверка атрибутов класса PlayList
    assert pl.title == "Moscow Python Meetup №81"
    assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"

    # Проверка метода total_duration
    try:
        duration = pl.total_duration
        print("Total Duration:", duration)
        assert isinstance(duration, datetime.timedelta)
        # Проверяем, что общая продолжительность составляет 11 минут и 40 секунд (660 секунд)
        assert duration.total_seconds() == 660.0
    except ValueError as e:
        print(e)

    # Проверка метода show_best_video
    try:
        assert pl.show_best_video() == "cUGyMzWQcGM"
    except ValueError as e:
        print(e)
