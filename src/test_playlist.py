# src/test_playlist.py

import datetime
from playlist import PlayList

def test_total_duration():
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    duration = pl.total_duration
    assert isinstance(duration, datetime.timedelta)


def test_best_video():
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    best_video_url = pl.show_best_video()
    assert best_video_url.startswith("https://youtu.be/")
