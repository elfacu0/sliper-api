import pytest
from scrapper import get_soup,get_channel_name
from models import Channel

class MockChannel:
    @staticmethod
    def urlopen():
        return open("fixtures/channel_fixture.txt", "r")

channel = Channel(name="Muzska89", subscribers="609K", views=151415059)
URL = "https://www.youtube.com/"
channelId = "@Muzska89"

class TestGetChannel:
    def test_get_name(self):
        url = URL + channelId + "/about"
        soup = get_soup(url)
        name = get_channel_name(soup)
        assert name == channel.name
