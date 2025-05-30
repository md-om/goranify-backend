# goranify-backend/main.py

import os
import sys

# این خط کمک می‌کنه پایتون ماژول‌های داخلی پروژه رو پیدا کنه
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # برای استفاده از List در Response Model ها
# ایمپورت کردن ماژول‌ها به صورت absolute (بدون نقطه اول)
import models, schemas, crud
import database
from fastapi.middleware.cors import CORSMiddleware

# ایجاد جداول در دیتابیس
# این خط باعث می‌شود که SQLAlchemy با استفاده از Base، جداول تعریف شده در models.py را در دیتابیس ایجاد کند.
# این عملیات فقط یک بار در زمان راه‌اندازی برنامه (اگر جداول موجود نباشند) انجام می‌شود.
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Goranify Music Downloader API",
    description="API for managing and downloading Kurdish music and related data.",
    version="0.1.0",
)

# تنظیمات CORS: این بخش برای ارتباط بین بک‌اند و فرانت‌اند لازمه
origins = [
    "http://localhost:8080",  # آدرس پیش‌فرض Vue.js dev server
    "http://localhost:5173",  # اگه از Vite استفاده می‌کنی
    # هر آدرس دیگری که پنل فرانت‌اندت بعداً روش دیپلوی میشه، اینجا اضافه کن
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # اجازه به تمام متدهای HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # اجازه به تمام هدرها
)


# Dependency برای گرفتن Session دیتابیس
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    """
    روت اصلی API، یک پیغام خوش‌آمدگویی برمی‌گرداند.
    """
    return {"message": "Welcome to Goranify Backend! Explore /docs for API endpoints."}


@app.get("/health")
async def health_check():
    """
    چک کردن وضعیت سلامت API.
    """
    return {"status": "ok", "message": "Backend is up and running!"}


# --- Advertisement Endpoints ---
@app.post("/advertisements/", response_model=schemas.Advertisement, status_code=status.HTTP_201_CREATED)
def create_advertisement(advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    """
    یک تبلیغ جدید اضافه می‌کند.
    """
    return crud.create_advertisement(db, advertisement)


@app.get("/advertisements/", response_model=List[schemas.Advertisement])
def read_advertisements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    لیستی از تبلیغات را دریافت می‌کند.
    """
    return crud.get_advertisements(db, skip=skip, limit=limit)


@app.get("/advertisements/{advertisement_id}", response_model=schemas.Advertisement)
def read_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    """
    جزئیات یک تبلیغ خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_advertisement = crud.get_advertisement(db, advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
    return db_advertisement


@app.put("/advertisements/{advertisement_id}", response_model=schemas.Advertisement)
def update_advertisement(advertisement_id: int, advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    """
    اطلاعات یک تبلیغ موجود را به‌روزرسانی می‌کند.
    """
    db_advertisement = crud.update_advertisement(db, advertisement_id, advertisement)
    if db_advertisement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
    return db_advertisement


@app.delete("/advertisements/{advertisement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    """
    یک تبلیغ را از دیتابیس حذف می‌کند.
    """
    db_advertisement = crud.delete_advertisement(db, advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Advertisement not found")
    return None


# --- Artist Endpoints ---
@app.post("/artists/", response_model=schemas.Artist, status_code=status.HTTP_201_CREATED)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    """
    یک خواننده جدید اضافه می‌کند.
    """
    return crud.create_artist(db, artist)


@app.get("/artists/", response_model=List[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    لیستی از خوانندگان را دریافت می‌کند.
    """
    return crud.get_artists(db, skip=skip, limit=limit)


@app.get("/artists/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    """
    جزئیات یک خواننده خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_artist = crud.get_artist(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return db_artist


@app.put("/artists/{artist_id}", response_model=schemas.Artist)
def update_artist(artist_id: int, artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    """
    اطلاعات یک خواننده موجود را به‌روزرسانی می‌کند.
    """
    db_artist = crud.update_artist(db, artist_id, artist)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return db_artist


@app.delete("/artists/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    """
    یک خواننده را از دیتابیس حذف می‌کند.
    """
    db_artist = crud.delete_artist(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return None


# --- Album Endpoints ---
@app.post("/albums/", response_model=schemas.Album, status_code=status.HTTP_201_CREATED)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    """
    یک آلبوم جدید اضافه می‌کند.
    """
    return crud.create_album(db, album)


@app.get("/albums/", response_model=List[schemas.Album])
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    لیستی از آلبوم‌ها را دریافت می‌کند.
    """
    return crud.get_albums(db, skip=skip, limit=limit)


@app.get("/albums/{album_id}", response_model=schemas.Album)
def read_album(album_id: int, db: Session = Depends(get_db)):
    """
    جزئیات یک آلبوم خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_album = crud.get_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return db_album


@app.put("/albums/{album_id}", response_model=schemas.Album)
def update_album(album_id: int, album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    """
    اطلاعات یک آلبوم موجود را به‌روزرسانی می‌کند.
    """
    db_album = crud.update_album(db, album_id, album)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return db_album


@app.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    """
    یک آلبوم را از دیتابیس حذف می‌کند.
    """
    db_album = crud.delete_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return None


# --- Genre Endpoints ---
@app.post("/genres/", response_model=schemas.Genre, status_code=status.HTTP_201_CREATED)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    """
    یک ژانر جدید اضافه می‌کند.
    """
    return crud.create_genre(db, genre)


@app.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    لیستی از ژانرها را دریافت می‌کند.
    """
    return crud.get_genres(db, skip=skip, limit=limit)


@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    جزئیات یک ژانر خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_genre = crud.get_genre(db, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return db_genre


@app.put("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    """
    اطلاعات یک ژانر موجود را به‌روزرسانی می‌کند.
    """
    db_genre = crud.update_genre(db, genre_id, genre)
    if db_genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return db_genre


@app.delete("/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    یک ژانر را از دیتابیس حذف می‌کند.
    """
    db_genre = crud.delete_genre(db, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return None


# --- Music Endpoints ---
@app.post("/musics/", response_model=schemas.Music, status_code=status.HTTP_201_CREATED)
def create_music(music: schemas.MusicCreate, db: Session = Depends(get_db)):
    """
    یک آهنگ جدید اضافه می‌کند.
    """
    return crud.create_music(db, music)


@app.get("/musics/", response_model=List[schemas.Music])
def read_musics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    لیستی از آهنگ‌ها را دریافت می‌کند.
    """
    return crud.get_musics(db, skip=skip, limit=limit)


@app.get("/musics/search/", response_model=List[schemas.Music])
def search_musics(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    آهنگ‌ها را بر اساس عنوان، خواننده یا آلبوم جستجو می‌کند.
    """
    return crud.search_musics(db, query, skip=skip, limit=limit)


@app.get("/musics/{music_id}", response_model=schemas.Music)
def read_music(music_id: int, db: Session = Depends(get_db)):
    """
    جزئیات یک آهنگ خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_music = crud.get_music(db, music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return db_music


@app.put("/musics/{music_id}", response_model=schemas.Music)
def update_music(music_id: int, music: schemas.MusicCreate, db: Session = Depends(get_db)):
    """
    اطلاعات یک آهنگ موجود را به‌روزرسانی می‌کند.
    """
    db_music = crud.update_music(db, music_id, music)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return db_music


@app.delete("/musics/{music_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_music(music_id: int, db: Session = Depends(get_db)):
    """
    یک آهنگ را از دیتابیس حذف می‌کند.
    """
    db_music = crud.delete_music(db, music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return None