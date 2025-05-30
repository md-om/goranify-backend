# goranify-backend/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func # برای timestamp خودکار
import database # ایمپورت کردن ماژول database برای دسترسی به Base

class Music(database.Base): # Music از database.Base (که از database.py میاد) ارث می‌برد
    __tablename__ = "musics" # اسم جدول در دیتابیس

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    album = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    download_url = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True) # مدت زمان بر حسب ثانیه (مثلاً 240 برای 4 دقیقه)
    created_at = Column(DateTime, server_default=func.now()) # زمان ایجاد رکورد (خودکار)
    updated_at = Column(DateTime, onupdate=func.now()) # زمان آخرین به‌روزرسانی (خودکار)