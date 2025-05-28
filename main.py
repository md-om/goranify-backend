# goranify-backend/main.py

import os
import sys

# این خط کمک می‌کنه پایتون ماژول‌های داخلی پروژه رو پیدا کنه
# (که بعداً برای database, models, schemas, crud استفاده می‌شه)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # برای ارتباط با فرانت‌اند

app = FastAPI(
    title="Goranify Music Downloader API",
    description="API for managing and downloading Kurdish music.",
    version="0.1.0",
)

# تنظیمات CORS: این بخش برای ارتباط بین بک‌اند و فرانت‌اند لازمه
# فعلاً برای محیط توسعه روی localhost:8080 تنظیم می‌کنیم
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