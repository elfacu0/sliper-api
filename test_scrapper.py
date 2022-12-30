import pytest
from scrapper import get_soup, get_channel_name, get_channel_subscribers, get_channel_views, get_channel_join_date, get_channel_data
from models import Channel


class MockChannel:
    @staticmethod
    def urlopen():
        return open("fixtures/channel_fixture.txt", "r")


channel = Channel(name="Muzska89", join_date="Mar 16, 2009",
                  subscribers="609K", views=151415059)
BASE_URL = "https://www.youtube.com/"
channel_id = "@Muzska89"

@pytest.fixture
def mock_channel_soup():
    url = BASE_URL + channel_id + "/about"
    return get_soup(url)


class TestGetChannel:
    def test_get_name(self):
        name = get_channel_name(mock_channel_soup)
        assert name == channel.name

    def test_get_subscribers(self):
        subscribers = get_channel_subscribers(mock_channel_soup)
        assert subscribers == channel.subscribers

    def test_get_views(self):
        views = get_channel_views(mock_channel_soup)
        assert views == channel.views

    def test_get_join_date(self):
        join_date = get_channel_join_date(mock_channel_soup)
        assert join_date == channel.join_date

    def test_get_channel_data(self):
        res_channel = get_channel_data(channel_id)
        assert res_channel == channel
