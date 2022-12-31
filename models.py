from pydantic import BaseModel

class Channel(BaseModel):
    name: str
    join_date: str
    views: str
    subscribers: str

class Video(BaseModel):
    title: str
    upload_date: str
    views: str
    likes: str

class Comment(BaseModel):
    user: str
    body: str
    likes: str

class Thumbnails(BaseModel):
    maxresdefault: str
    hqdefault: str