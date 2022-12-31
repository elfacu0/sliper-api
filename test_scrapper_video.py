import pytest
import urllib.request as request
from scrapper import get_soup, get_video_title, get_video_date, get_video_views, get_video_likes, get_video_data
from models import Video


def mock_urlopen(url: str):
    return open("fixtures/video_fixture.txt", "r")


video = Video(title="PONIENDO A PARIR FALLOUT 4",
              upload_date="19 nov 2015", views="2,493,264", likes="71,233")
BASE_URL = "https://www.youtube.com/"
video_id = "1vQuHvXX550"


def mock_channel_soup():
    url = BASE_URL + "watch?v=" + video_id
    return get_soup(url)


class TestGetChannel:
    def test_get_video_title(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        title = get_video_title(mock_channel_soup())
        assert title == video.title

    def test_get_video_date(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        upload_date = get_video_date(mock_channel_soup())
        assert upload_date == video.upload_date

    def test_get_video_views(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        views = get_video_views(mock_channel_soup())
        assert views == video.views

    def test_get_video_likes(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        likes = get_video_likes(mock_channel_soup())
        assert likes == video.likes

    def test_get_video_data(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        res_video = get_video_data(video_id)
        assert res_video == video
