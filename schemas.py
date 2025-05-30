# goranify-backend/schemas.py

from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Base Schema برای داده‌های مشترک (مثلاً برای ایجاد و به‌روزرسانی)
class MusicBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    cover_url: Optional[HttpUrl] = None # HttpUrl برای اعتبار سنجی فرمت URL
    download_url: HttpUrl
    source_url: Optional[HttpUrl] = None
    duration: Optional[int] = None # مدت زمان بر حسب ثانیه

# Schema برای ایجاد یک آهنگ جدید
class MusicCreate(MusicBase):
    pass # فعلاً شبیه MusicBase است، اگر بعداً فیلدهای خاصی برای ایجاد نیاز شد اینجا اضافه میشه

# Schema برای پاسخ API (زمانی که یک آهنگ را برمی‌گردانیم)
class Music(MusicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # from_attributes = True: به Pydantic می‌گوید می‌تواند داده را از یک ORM مثل SQLAlchemy بخواند
        from_attributes = True
        # alias_generator = to_camel: اگر نیاز به camelCase در JSON داشتیم
        # allow_population_by_field_name = True: اجازه می‌دهد با field_name هم مقداردهی شود