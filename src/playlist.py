import datetime

class Video:
    def __init__(self, video_id, title=None, like_count=None, duration=None):
        self.video_id = video_id
        self.title = title
        self.like_count = like_count
        self.duration = duration
class PlayList:
    def __init__(self, playlist_id, title=None, url=None, videos=None):
        self.playlist_id = playlist_id
        self.title = title
        self.url = url
        self.videos = videos

    @property
    def total_duration(self):
        # Рассчет общей длительности видео в плейлисте
        total_duration = sum(video.duration for video in self.videos if video.duration)
        return datetime.timedelta(seconds=total_duration)

    def show_best_video(self):
        # Поиск самого популярного видео по количеству лайков
        best_video = max(self.videos, key=lambda video: video.like_count)
        return best_video.video_id if best_video else None
