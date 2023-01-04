import pytest
import urllib.request as request
from scrapper import get_soup, get_channel_name, get_channel_subscribers, get_channel_views, get_channel_join_date, get_channel_data, get_channel_avatar_data
from models import Channel, Avatar


def mock_urlopen(url: str):
    return open("fixtures/channel_fixture.txt", "r")


channel = Channel(name="Muzska89", join_date="16 mar 2009",
                  subscribers="609,000", views="151,423,488")
avatar = Avatar(
    url="https://yt3.googleusercontent.com/ytc/AMLnZu-zAP4lxzap20jm-b81Q2aOiXEygPMdFU9n_-gKdQ=s176-c-k-c0x00ffffff-no-rj")
BASE_URL = "https://www.youtube.com/"
channel_id = "@Muzska89"


def mock_channel_soup():
    url = BASE_URL + channel_id + "/about"
    return get_soup(url)


class TestGetChannel:
    def test_get_name(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        name = get_channel_name(mock_channel_soup())
        assert name == channel.name

    def test_get_subscribers(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        subscribers = get_channel_subscribers(mock_channel_soup())
        assert subscribers == channel.subscribers

    def test_get_views(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        views = get_channel_views(mock_channel_soup())
        assert views == channel.views

    def test_get_join_date(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        join_date = get_channel_join_date(mock_channel_soup())
        assert join_date == channel.join_date

    def test_get_channel_data(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        res_channel = get_channel_data(channel_id)
        assert res_channel == channel

    def test_get_channel_avatar_data(self, monkeypatch):
        monkeypatch.setattr(request, "urlopen", mock_urlopen)
        res_avatar = get_channel_avatar_data(channel_id)
        assert res_avatar == avatar
