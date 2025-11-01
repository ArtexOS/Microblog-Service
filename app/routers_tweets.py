from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List

from app import schemas
from app.models import Tweet, User, Like, Media, tweet_media, Follow
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/api", tags=["tweets"])

@router.post("/tweets", response_model=dict)
def create_tweet(payload: schemas.TweetCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tweet = Tweet(content=payload.tweet_data, author_id=user.id)
    db.add(tweet)
    db.flush()  # get id

    if payload.tweet_media_ids:
        medias = db.query(Media).filter(Media.id.in_(payload.tweet_media_ids)).all()
        for m in medias:
            db.execute(tweet_media.insert().values(tweet_id=tweet.id, media_id=m.id))

    db.commit()
    return {"result": True, "tweet_id": tweet.id}

@router.delete("/tweets/{tweet_id}", response_model=schemas.Result)
def delete_tweet(tweet_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(404, "Tweet not found")
    if tweet.author_id != user.id:
        raise HTTPException(403, "You can delete only your tweets")
    db.delete(tweet)
    db.commit()
    return {"result": True}

@router.post("/tweets/{tweet_id}/likes", response_model=schemas.Result)
def like_tweet(tweet_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(404, "Tweet not found")
    exists = db.query(Like).filter(Like.user_id == user.id, Like.tweet_id == tweet_id).first()
    if not exists:
        db.add(Like(user_id=user.id, tweet_id=tweet_id))
        db.commit()
    return {"result": True}

@router.delete("/tweets/{tweet_id}/likes", response_model=schemas.Result)
def unlike_tweet(tweet_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    like = db.query(Like).filter(Like.user_id == user.id, Like.tweet_id == tweet_id).first()
    if like:
        db.delete(like)
        db.commit()
    return {"result": True}

@router.get("/tweets", response_model=schemas.TweetsResp)
def get_feed(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    sub_following = db.query(Follow.followee_id).filter(Follow.follower_id == user.id).subquery()
    like_count = func.count(Like.user_id).label("likes_cnt")
    q = (
        db.query(Tweet, like_count)
        .outerjoin(Like, Like.tweet_id == Tweet.id)
        .filter(Tweet.author_id.in_(select(sub_following.c.followee_id)))
        .group_by(Tweet.id)
        .order_by(like_count.desc(), Tweet.created_at.desc())
        .all()
    )

    tweets_out: List[schemas.TweetOut] = []
    for tweet, _ in q:
        author = db.query(User).filter(User.id == tweet.author_id).first()
        likes_rows = db.query(Like, User).join(User, User.id == Like.user_id).filter(Like.tweet_id == tweet.id).all()
        likes = [schemas.LikeDTO(user_id=u.id, name=u.name) for _, u in likes_rows]
        medias = (
            db.query(Media)
            .join(tweet_media, tweet_media.c.media_id == Media.id)
            .filter(tweet_media.c.tweet_id == tweet.id)
            .all()
        )
        attachments = [f"/media/{m.id}" for m in medias]
        tweets_out.append(
            schemas.TweetOut(
                id=tweet.id,
                content=tweet.content,
                attachments=attachments,
                author=schemas.Author(id=author.id, name=author.name),
                likes=likes,
            )
        )
    return {"result": True, "tweets": tweets_out}
