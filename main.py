from fastapi import FastAPI, HTTPException, status, Depends
from models import Channel, Video, Comment, Thumbnails, Token
from scrapper import get_channel_data, get_video_data, get_video_thumbnails_json
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "f139c7af6c971c6afa622944223181173e10572a9849b1778bfa409460eb0f45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

description = """
With **Sliper API** you can easily retrieve information about specific YouTube videos and channels, including the number of likes, views, and subscribers, as well as the title and name of the video or channel. This information can be used in a variety of ways, such as to display the most popular videos or channels, or to track the performance of a particular video or channel over time.

## Channels

Get stats about youtube **Channel**.

* Name
* Join Date
* Views
* Subscribers

## Videos

You will be able to:

* **Get Video Stats**
* **Get Video Thumbnail**
* **Get Video Comments** (_not implemented_).

## Authorization

This API requires an authorization token to be included in the header of every request. The token must be sent in the Authorization header, in the following format: 

```http
  Authorization: Bearer <TOKEN>.
```

The authentication token has a expiration time of 15 minutes. If a request is made with an expired token, the API will return a 401 Unauthorized error. To continue using the API, you will need to request a new token.

## Live Preview

You can try all endpoints by clicking the "Try it out" button, but before that you must set the authorization token

Click the "Authorize" Button bellow and without filling the inputs click the "authorize" button  (Remember that tokens expire after 15 minutes)




"""

tags_metadata = [
    {
        "name": "Auth",
        "description": "To use this API you must have a Bearer Token, create it here",
    },
    {
        "name": "Channel",
        "description": "Get youtube channel stats.",
    },
    {
        "name": "Video",
        "description": "Get youtube video stats and thumbnails.",
    },
]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Token",
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"Sliper": "Get youtube videos and channel data", "READ": "The docs for more information"}


@ app.post("/token", response_model=Token)
def login():
    return create_access_token()


@ app.get("/auth", response_model=Token, tags=["Auth"])
def get_auth_token():
    return create_access_token()


@app.get("/channel/{channel_id}", tags=["Channel"], response_model=Channel)
def get_channel(channel_id: str, token: str = Depends(oauth2_scheme)):
    """
    Returns stats of the given Channel

    channel_id must include the at sign E.g. @Muzska89
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
def get_video_stats(video_id: str, token: str = Depends(oauth2_scheme)):
    """
    Returns stats of the given Video

    you can find the video_id after the "v" query 

    https://www.youtube.com/watch?v=**2Z5AEVX1lLQ**
    """
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
    """
    Returns the thumbnail of the given video in various sizes

    You don't need use a token in this one
    """
    return get_video_thumbnails_json(video_id)


def create_access_token() -> Token:
    expire = (datetime.utcnow() + timedelta(minutes=15)).timestamp()
    encoded_jwt = jwt.encode({"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    token = Token(access_token=encoded_jwt, token_type="bearer")
    return token


def is_valid_token(jwt_token: str) -> bool:
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=ALGORITHM)
        exp_seconds = payload["exp"]
        current_seconds = datetime.utcnow().timestamp()
        return current_seconds < exp_seconds
    except JWTError:
        return False
