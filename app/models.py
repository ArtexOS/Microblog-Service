from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Table, DateTime, func, Column
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    api_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")

class Media(Base):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)

tweet_media = Table(
    "tweet_media",
    Base.metadata,
    Column("tweet_id", ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", ForeignKey("medias.id", ondelete="CASCADE"), primary_key=True),
)

class Tweet(Base):
    __tablename__ = "tweets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    author = relationship("User", back_populates="tweets")
    media: Mapped[List["Media"]] = relationship("Media", secondary=tweet_media)

class Like(Base):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)

class Follow(Base):
    __tablename__ = "follows"
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    followee_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
