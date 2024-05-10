from src.video import Video

if __name__ == '__main__':
    api_key = "AIzaSyDwuxvkIC_OTUYnAiBOAsgUDtAEBb6iuug"
    broken_video = Video('broken_video_id', api_key)
    assert broken_video.title is None
    assert broken_video.like_count is None
    assert broken_video.duration is None