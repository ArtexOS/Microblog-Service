from app.db import SessionLocal, engine
from app.models import Base, User, Follow, Tweet, Like
from app.config import settings

def run_seed():
    if not settings.SEED_ON_STARTUP:
        return
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        users = [
            {"name": "Alice", "api_key": "alice-key"},
            {"name": "Bob", "api_key": "bob-key"},
            {"name": "Carol", "api_key": "carol-key"},
        ]
        for u in users:
            if not db.query(User).filter(User.api_key == u["api_key"]).first():
                db.add(User(name=u["name"], api_key=u["api_key"]))
        db.commit()

        alice = db.query(User).filter(User.api_key == "alice-key").first()
        bob = db.query(User).filter(User.api_key == "bob-key").first()
        carol = db.query(User).filter(User.api_key == "carol-key").first()

        if alice and bob and not db.query(Follow).filter_by(follower_id=alice.id, followee_id=bob.id).first():
            db.add(Follow(follower_id=alice.id, followee_id=bob.id))
        if alice and carol and not db.query(Follow).filter_by(follower_id=alice.id, followee_id=carol.id).first():
            db.add(Follow(follower_id=alice.id, followee_id=carol.id))
        db.commit()

        if bob and not db.query(Tweet).filter(Tweet.author_id == bob.id).first():
            db.add_all([
                Tweet(content="Hello from Bob!", author_id=bob.id),
                Tweet(content="Another day, another tweet", author_id=bob.id),
            ])
        if carol and not db.query(Tweet).filter(Tweet.author_id == carol.id).first():
            db.add(Tweet(content="Carol here, posting a pic soon!", author_id=carol.id))
        db.commit()

        bob = db.merge(bob)
        carol = db.merge(carol)
        tweets = db.query(Tweet).all()
        for t in tweets:
            if not db.query(Like).filter_by(user_id=alice.id, tweet_id=t.id).first():
                db.add(Like(user_id=alice.id, tweet_id=t.id))
        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
