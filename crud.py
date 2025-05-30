# goranify-backend/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import or_ # برای جستجو
import models, schemas # ایمپورت کردن ماژول‌ها به صورت absolute

# --- Create (ایجاد) ---
def create_music(db: Session, music: schemas.MusicCreate):
    """
    آهنگ جدیدی را در دیتابیس ایجاد می‌کند.
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
    db.commit() # تغییرات را در دیتابیس ذخیره می‌کند
    db.refresh(db_music) # شیء را با داده‌های جدید از دیتابیس (مثل ID و timestamp) به‌روزرسانی می‌کند
    return db_music

# --- Read (خواندن) ---
def get_music(db: Session, music_id: int):
    """
    یک آهنگ را بر اساس ID آن از دیتابیس دریافت می‌کند.
    """
    return db.query(models.Music).filter(models.Music.id == music_id).first()

def get_musics(db: Session, skip: int = 0, limit: int = 100):
    """
    لیستی از آهنگ‌ها را از دیتابیس دریافت می‌کند. قابلیت صفحه‌بندی (pagination) دارد.
    """
    return db.query(models.Music).offset(skip).limit(limit).all()

# --- Search (جستجو) ---
def search_musics(db: Session, query: str, skip: int = 0, limit: int = 100):
    """
    آهنگ‌ها را بر اساس عنوان یا نام خواننده جستجو می‌کند.
    """
    # جستجو در فیلدهای title و artist
    # از lower() برای جستجوی Case-Insensitive استفاده می‌کنیم
    # از ilike() برای جستجوی Case-Insensitive با الگو (pattern matching) استفاده می‌کنیم
    search_pattern = f"%{query.lower()}%"
    return (
        db.query(models.Music)
        .filter(
            or_(
                models.Music.title.ilike(search_pattern),
                models.Music.artist.ilike(search_pattern),
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


# --- Update (به‌روزرسانی) ---
def update_music(db: Session, music_id: int, music_data: schemas.MusicCreate):
    """
    اطلاعات یک آهنگ موجود را به‌روزرسانی می‌کند.
    """
    db_music = db.query(models.Music).filter(models.Music.id == music_id).first()
    if db_music:
        # فیلدهایی که باید به‌روزرسانی شوند را اعمال می‌کنیم
        # model_dump(exclude_unset=True) فقط فیلدهایی که در Request Body ارسال شده‌اند را برمی‌گرداند
        # این کار جلوی بازنویسی فیلدهای خالی را می‌گیرد
        for key, value in music_data.model_dump(exclude_unset=True).items():
            setattr(db_music, key, value)
        db.commit()
        db.refresh(db_music)
        return db_music
    return None # اگر آهنگ پیدا نشد

# --- Delete (حذف) ---
def delete_music(db: Session, music_id: int):
    """
    یک آهنگ را بر اساس ID آن از دیتابیس حذف می‌کند.
    """
    db_music = db.query(models.Music).filter(models.Music.id == music_id).first()
    if db_music:
        db.delete(db_music)
        db.commit()
        return {"message": "Music deleted successfully"}
    return None # اگر آهنگ پیدا نشد