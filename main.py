from fastapi import FastAPI, HTTPException, status
from models import Channel, Video, Comment, Thumbnails, Token
from scrapper import get_channel_data, get_video_data, get_video_thumbnails_json
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "f139c7af6c971c6afa622944223181173e10572a9849b1778bfa409460eb0f45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

description = """
Sliper API allows you to get all data about youtube channels and videos

## Channels

You can get all stats about youtube **Channels**.

## Videos

You will be able to:

* **Get Video Stats**
* **Get Video Thumbnail**
* **Get Video Comments** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Auth",
        "description": "To use the endpoints you must have a Token, create it here",
    },
    {
        "name": "Channel",
        "description": "Get youtube channel stats.",
    },
    {
        "name": "Video",
        "description": "Get video stats and thumbnails.",
    },
]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token Invalid",
    headers={"WWW-Authenticate": "Bearer"},
)


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
    return {"Sliper": "Get youtube videos and channel data", "READ": "The docs for more information"}

@ app.get("/auth", response_model=Token, tags=["Auth"])
def get_auth_token():
    return create_access_token()

@app.get("/channel/{channel_id}", tags=["Channel"], response_model=Channel)
def get_channel(channel_id: str, token: str):
    """
    Returns stats of the given Channel

    Channel_id must include the at sign E.g. @Muzska89
    """
    if not is_valid_token(token):
        raise credentials_exception
    try:
        return get_channel_data(channel_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


@ app.get("/video/{video_id}", tags=["Video"], response_model=Video)
def get_video_stats(video_id: str, token: str):
    if not is_valid_token(token):
        raise credentials_exception
    try:
        return get_video_data(video_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


# @ app.get("/video/comments/{video_id}", tags=["video"], response_model=[Comment])
# def get_video_comments(video_id: str):
#     return


@ app.get("/video/thumbnail/{video_id}", tags=["Video"], response_model=Thumbnails)
def get_video_thumbnails(video_id: str):
    return get_video_thumbnails_json(video_id)


def create_access_token() -> Token:
    expire = datetime.utcnow() + timedelta(minutes=15)
    encoded_jwt = jwt.encode({"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    token = Token(access_token=encoded_jwt, token_type="bearer")
    return token


def is_valid_token(jwt_token: str) -> bool:
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=ALGORITHM)
        exp = payload["exp"]
        print(exp)
        return True
    except JWTError:
        return False