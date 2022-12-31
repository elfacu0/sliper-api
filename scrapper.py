import urllib.request as request
from bs4 import BeautifulSoup
from models import Channel, Video
import json

URL = "https://www.youtube.com/"


def get_soup(url: str) -> BeautifulSoup:
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    return soup

# def saveSoup():
#     f = open("demofile3.txt", "w", encoding='utf-8')
#     f.write(str(soup))
#     f.close()


def find_key(obj, key):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                return v
            else:
                result = find_key(v, key)
                if result is not None:
                    return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_key(item, key)
            if result is not None:
                return result
    return None


def find_key_parent(obj, key):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                return obj
            else:
                result = find_key_parent(v, key)
                if result is not None:
                    return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_key_parent(item, key)
            if result is not None:
                return result
    return None


def get_channel_name(soup: BeautifulSoup) -> str:
    script = soup.find_all("script")[33].text
    name = find_key_parent(json.loads(
        script[19:-1]), "bypassBusinessEmailCaptcha")['title']['simpleText']
    return name


def get_channel_subscribers(soup: BeautifulSoup) -> str:
    script = soup.find_all("script")[33].text
    str_subscribers = find_key(json.loads(
        script[19:-1]), "subscriberCountText")['simpleText']
    subscribers = str_subscribers.split(" ")[0]
    return subscribers


def get_channel_views(soup: BeautifulSoup) -> str:
    script = soup.find_all("script")[33].text
    str_views = find_key(json.loads(
        script[19:-1]), "viewCountText")["simpleText"]
    views = str_views.split(" ")[0]
    print(views)
    return views


def get_channel_join_date(soup: BeautifulSoup) -> str:
    script = soup.find_all("script")[33].text
    str_join_date = find_key(json.loads(
        script[19:-1]), "joinedDateText")['runs']
    join_date = str_join_date[1]['text']
    return join_date


def get_channel_data(id: str) -> Channel:
    url = URL + id + "/about"
    soup = get_soup(url)
    channel = Channel(name=get_channel_name(soup), join_date=get_channel_join_date(soup),
                      subscribers=get_channel_subscribers(soup), views=get_channel_views(soup))
    return channel


def get_video_script_data(soup: BeautifulSoup):
    script = soup.find_all("script")[43].text
    jsonLoad = json.loads(script[19:-1])
    jsonData = find_key(jsonLoad, "videoDescriptionHeaderRenderer")
    return jsonData


def get_video_title(soup: BeautifulSoup) -> str:
    script_data = get_video_script_data(soup)
    title = script_data['title']['runs'][0]['text']
    return title


def get_video_date(soup: BeautifulSoup) -> str:
    script_data = get_video_script_data(soup)
    upload_date = script_data['publishDate']['simpleText']
    return upload_date


def get_video_views(soup: BeautifulSoup) -> str:
    script_data = get_video_script_data(soup)
    views = script_data['factoid'][1]['factoidRenderer']['value']['simpleText']
    return views


def get_video_likes(soup: BeautifulSoup) -> str:
    script_data = get_video_script_data(soup)
    views = script_data['factoid'][0]['factoidRenderer']['value']['simpleText']
    return views


def get_video_data(id: str) -> Video:
    url = URL + "watch?v=" + id
    soup = get_soup(url)
    video = Video(title=get_video_title(soup), upload_date=get_video_date(
        soup), views=get_video_views(soup), likes=get_video_likes(soup))
    return video


def get_video_thumbnails_json(id: str) -> str:
    return {'maxresdefault': f'https://i.ytimg.com/vi/{id}/maxresdefault.jpg', "hqdefault": f'https://i.ytimg.com/vi/{id}/hqdefault.jpg'}
