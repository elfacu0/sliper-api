from fastapi import FastAPI
from models import Channel, Video, Comment, Thumbnails
from scrapper import get_channel_data, get_video_data, get_video_thumbnails_json

description = """
Sliper API allows you to get all data about youtube channels and videos

## Channels

You can get all data about youtube **Channels**.

## Videos

You will be able to:

* **Get Video Stats** (_not implemented_).
* **Get Video Comments** (_not implemented_).
* **Get Video Thumbnail** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "channel",
        "description": "Get data about channel.",
    },
    {
        "name": "video",
        "description": "Get data about video.",
    },
]


app = FastAPI(title="Sliper",
              description=description,
              version="0.0.1",
              contact={
                      "name": "Gitlab",
                      "url": "http://x-force.example.com/contact/",
              },
              openapi_tags=tags_metadata)


@app.get("/")
def read_root():
    return {"Sliper": "Get youtube videos and channel data"}


@app.get("/channel/{channel_id}", tags=["channel"], response_model=Channel)
def get_channel(channel_id: str):
    return get_channel_data(channel_id)


@ app.get("/video/{video_id}", tags=["video"], response_model=Video)
def get_video_stats(video_id: str):
    return get_video_data(video_id)


# @ app.get("/video/comments/{video_id}", tags=["video"], response_model=[Comment])
# def get_video_comments(video_id: str):
#     return


@ app.get("/video/thumbnail/{video_id}", tags=["video"], response_model=Thumbnails)
def get_video_thumbnails(video_id: str):
    return get_video_thumbnails_json(video_id)
