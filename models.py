# goranify-backend/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import database # برای دسترسی به Base


class Advertisement(database.Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    cover_url = Column(String, nullable=True) # URL تصویر یا کاور تبلیغ
    sponsor = Column(String, nullable=True)


class Artist(database.Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    birth_date = Column(DateTime, nullable=True)
    is_alive = Column(Boolean, default=True)
    death_date = Column(DateTime, nullable=True) # فقط در صورت is_alive = False
    biography = Column(Text, nullable=True)

    # روابط با جداول دیگر
    albums = relationship("Album", back_populates="artist")
    musics = relationship("Music", back_populates="artist")


class Album(database.Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    cover_url = Column(String, nullable=True) # URL کاور آلبوم
    release_year = Column(Integer, nullable=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False) # ارتباط با جدول Artist

    # روابط با جداول دیگر
    artist = relationship("Artist", back_populates="albums")
    musics = relationship("Music", back_populates="album")


class Genre(database.Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True) # نام ژانر باید یکتا باشد

    # رابطه با جدول Music
    musics = relationship("Music", back_populates="genre")


class Music(database.Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True) # ارتباط با جدول Album
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False) # ارتباط با جدول Artist
    cover_url = Column(String, nullable=True) # کاور یا تصویر آهنگ (اگه از آلبوم جدا باشه)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=True) # ارتباط با جدول Genre
    lyrics = Column(Text, nullable=True)
    audio_128_url = Column(String, nullable=False) # آدرس آهنگ با کیفیت 128
    audio_320_url = Column(String, nullable=False) # آدرس آهنگ با کیفیت 320
    # سال انتشار از جدول آلبوم گرفته می‌شود و نیازی به ذخیره مستقیم ندارد

    # روابط با جداول دیگر
    album = relationship("Album", back_populates="musics")
    artist = relationship("Artist", back_populates="musics")
    genre = relationship("Genre", back_populates="musics")