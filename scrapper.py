import urllib.request as request
from bs4 import BeautifulSoup
from models import Channel

URL = "https://www.youtube.com/"

def get_soup(url: str) -> BeautifulSoup:
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_channel_data(id: str) -> Channel:
    url = URL + id + "/about"
    soup = get_soup(url)
    return

def get_channel_name(soup: BeautifulSoup) -> str:
    return "Muzska89"

def get_channel_subscribers(soup: BeautifulSoup) -> str:
    return "609K"

def get_channel_views(soup: BeautifulSoup) -> int:
    return 151415059