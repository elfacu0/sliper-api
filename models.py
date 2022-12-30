from pydantic import BaseModel

class Channel(BaseModel):
    name: str
    join_date: str
    views: int
    subscribers: str