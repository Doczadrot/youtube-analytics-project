import datetime
import requests
import urllib.parse

class Video:
    def __init__(self, video_id, api_key):
        self.video_id = video_id
        self.title = None
        self.like_count = None
        self.duration = None

        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,statistics,contentDetails"
            response = requests.get(url)
            response.raise_for_status()

            video_data = response.json()["items"][0]
            self.title = video_data["snippet"]["title"]
            self.like_count = video_data["statistics"].get("likeCount", 0)
            duration = video_data["contentDetails"]["duration"]
            self.duration = parse_duration(duration)
        except (IndexError, KeyError, requests.exceptions.RequestException):
            pass

class PlayList:
    def __init__(self, playlist_id, api_key):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.videos = []

        try:
            url = f"https://www.googleapis.com/youtube/v3/playlists?id={playlist_id}&key={api_key}&part=snippet"
            response = requests.get(url)
            response.raise_for_status()

            playlist_data = response.json()["items"][0]
            self.title = playlist_data["snippet"]["title"]
            self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

            for video_id in self.get_video_ids(api_key):
                video = Video(video_id, api_key)
                self.videos.append(video)
        except (IndexError, KeyError, requests.exceptions.RequestException):
            pass

    def get_video_ids(self, api_key: str) -> list[str]:
        video_ids = []
        next_page_token = None

        while True:
            url_params = {
                "playlistId": self.playlist_id,
                "key": api_key,
                "part": "contentDetails",
                "maxResults": 50,
            }
            if next_page_token:
                url_params["pageToken"] = next_page_token

            url = f"https://www.googleapis.com/youtube/v3/playlistItems?{urllib.parse.urlencode(url_params)}"
            response = requests.get(url)
            response.raise_for_status()

            for item in response.json()["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = response.json().get("nextPageToken")
            if not next_page_token:
                break

        return video_ids

    @property
    def total_duration(self):
        total_seconds = sum(video.duration.total_seconds() for video in self.videos if video.duration is not None)
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video.like_count or 0)
        return f"https://youtu.be/{best_video.video_id}" if best_video else None

def parse_duration(duration_str):
    duration_components = duration_str.split("PT")[1].split("M")
    hours = int(duration_components[0]) if duration_components[0] else 0
    minutes = int(duration_components[1].split("S")[0]) if len(duration_components) > 1 and duration_components[1] else 0
    seconds = int(duration_components[-1][:-1]) if len(duration_components) > 1 and duration_components[-1][-1] == "S" else 0
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

if __name__ == '__main__':
    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw', api_key)

    assert pl.title == "Moscow Python Meetup №81"
    assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"

    duration = pl.total_duration
    assert str(duration) == "1:49:52"
    assert isinstance(duration, datetime.timedelta)
    assert duration.total_seconds() == 6592.0

    assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"