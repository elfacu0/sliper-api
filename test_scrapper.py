import pytest
from scrapper import get_soup, get_channel_name, get_channel_subscribers
from models import Channel


class MockChannel:
    @staticmethod
    def urlopen():
        return open("fixtures/channel_fixture.txt", "r")


channel = Channel(name="Muzska89", join_date="Mar 16, 2009",
                  subscribers="609K", views=151415059)
BASE_URL = "https://www.youtube.com/"

@pytest.fixture
def mock_channel_soup():
    channelId = "@Muzska89"
    url = BASE_URL + channelId + "/about"
    return get_soup(url)

class TestGetChannel:
    def test_get_name(self):
        name = get_channel_name(mock_channel_soup)
        assert name == channel.name

    def test_get_subscribers(self):
        subscribers = get_channel_subscribers(mock_channel_soup)
        assert subscribers == channel.subscribers
