from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.models import User, Follow
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/api", tags=["users"])

def _user_out(db: Session, user: User) -> schemas.UserOut:
    followers = db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followee_id == user.id).all()
    following = db.query(User).join(Follow, Follow.followee_id == User.id).filter(Follow.follower_id == user.id).all()
    return schemas.UserOut(
        id=user.id,
        name=user.name,
        followers=[schemas.UserBrief(id=u.id, name=u.name) for u in followers],
        following=[schemas.UserBrief(id=u.id, name=u.name) for u in following],
    )

@router.get("/users/me", response_model=schemas.UserResp)
def me(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"result": True, "user": _user_out(db, user)}

@router.get("/users/{user_id}", response_model=schemas.UserResp)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return {"result": True, "user": _user_out(db, user)}

@router.post("/users/{user_id}/follow", response_model=schemas.Result)
def follow(user_id: int, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    if me.id == user_id:
        return {"result": True}
    exists = db.query(Follow).filter(Follow.follower_id == me.id, Follow.followee_id == user_id).first()
    if not exists:
        db.add(Follow(follower_id=me.id, followee_id=user_id))
        db.commit()
    return {"result": True}

@router.delete("/users/{user_id}/follow", response_model=schemas.Result)
def unfollow(user_id: int, db: Session = Depends(get_db), me: User = Depends(get_current_user)):
    rel = db.query(Follow).filter(Follow.follower_id == me.id, Follow.followee_id == user_id).first()
    if rel:
        db.delete(rel)
        db.commit()
    return {"result": True}
