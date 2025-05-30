# goranify-backend/main.py

import os
import sys

# این خط کمک می‌کنه پایتون ماژول‌های داخلی پروژه رو پیدا کنه
# (مثلاً models, schemas, crud, database)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
# ایمپورت کردن ماژول‌ها به صورت absolute (بدون نقطه اول)
import models, schemas # ماژول crud رو هم آماده می‌کنیم، گرچه هنوز خالیه
import database # ماژول database برای دسترسی به engine و get_db و Base
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

# --- API Endpoints برای مدیریت موزیک‌ها (فعلاً برای تست، بعداً به crud منتقل می‌شوند) ---

@app.post("/musics/", response_model=schemas.Music, status_code=status.HTTP_201_CREATED)
def create_music_endpoint(music: schemas.MusicCreate, db: Session = Depends(database.get_db)):
    """
    یک آهنگ جدید را به دیتابیس اضافه می‌کند. (این تابع موقتی است و به crud.py منتقل خواهد شد)
    """
    db_music = models.Music(
        title=music.title,
        artist=music.artist,
        album=music.album,
        cover_url=music.cover_url,
        download_url=music.download_url,
        source_url=music.source_url,
        duration=music.duration
    )
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music

@app.get("/musics/", response_model=list[schemas.Music])
def read_musics_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    لیستی از آهنگ‌ها را دریافت می‌کند. قابلیت صفحه‌بندی (pagination) دارد. (این تابع موقتی است و به crud.py منتقل خواهد شد)
    """
    musics = db.query(models.Music).offset(skip).limit(limit).all()
    return musics