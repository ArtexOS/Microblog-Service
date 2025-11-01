from pydantic import BaseModel, Field
from typing import List, Optional

class Result(BaseModel):
    result: bool = True

class ErrorResp(BaseModel):
    result: bool = False
    error_type: str
    error_message: str

class Author(BaseModel):
    id: int
    name: str

class LikeDTO(BaseModel):
    user_id: int
    name: str

class TweetCreate(BaseModel):
    tweet_data: str = Field(..., min_length=1, max_length=280)
    tweet_media_ids: Optional[List[int]] = None

class TweetOut(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: Author
    likes: List[LikeDTO] = []

class UserBrief(BaseModel):
    id: int
    name: str

class UserOut(BaseModel):
    id: int
    name: str
    followers: List[UserBrief]
    following: List[UserBrief]

class UserResp(BaseModel):
    result: bool = True
    user: UserOut

class TweetsResp(BaseModel):
    result: bool = True
    tweets: List[TweetOut]
