# goranify-backend/main.py

import os
import sys

# این خط کمک می‌کنه پایتون ماژول‌های داخلی پروژه رو پیدا کنه
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    description="API for managing and downloading Kurdish music.",
    version="0.1.0",
)

# تنظیمات CORS
origins = [
    "http://localhost:8080", # آدرس پیش‌فرض Vue.js dev server
    # "http://localhost:5173", # اگه از Vite استفاده می‌کنی
    # آدرس‌های دیگه رو هم اینجا اضافه کن بعداً (بعد از deploy)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # اجازه به تمام متدهای HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # اجازه به تمام هدرها
)

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

# --- API Endpoints برای مدیریت موزیک‌ها ---

@app.post("/musics/", response_model=schemas.Music, status_code=status.HTTP_201_CREATED)
def create_music_endpoint(music: schemas.MusicCreate, db: Session = Depends(database.get_db)):
    """
    یک آهنگ جدید را به دیتابیس اضافه می‌کند.
    """
    return crud.create_music(db=db, music=music)

@app.get("/musics/", response_model=list[schemas.Music])
def read_musics_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    لیستی از آهنگ‌ها را دریافت می‌کند. قابلیت صفحه‌بندی (pagination) دارد.
    """
    musics = crud.get_musics(db, skip=skip, limit=limit)
    return musics

@app.get("/musics/search/", response_model=list[schemas.Music])
def search_musics_endpoint(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    آهنگ‌ها را بر اساس عنوان یا نام خواننده جستجو می‌کند.
    """
    musics = crud.search_musics(db, query=query, skip=skip, limit=limit)
    return musics

@app.get("/musics/{music_id}", response_model=schemas.Music)
def read_music_endpoint(music_id: int, db: Session = Depends(database.get_db)):
    """
    جزئیات یک آهنگ خاص را بر اساس ID آن دریافت می‌کند.
    """
    db_music = crud.get_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return db_music

@app.put("/musics/{music_id}", response_model=schemas.Music)
def update_music_endpoint(music_id: int, music: schemas.MusicCreate, db: Session = Depends(database.get_db)):
    """
    اطلاعات یک آهنگ موجود را به‌روزرسانی می‌کند.
    """
    db_music = crud.update_music(db, music_id=music_id, music_data=music)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return db_music

@app.delete("/musics/{music_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_music_endpoint(music_id: int, db: Session = Depends(database.get_db)):
    """
    یک آهنگ را از دیتابیس حذف می‌کند.
    """
    db_music = crud.delete_music(db, music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return None # 204 No Content پاسخ می‌دهد