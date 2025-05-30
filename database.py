# goranify-backend/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# لود کردن متغیرهای محیطی از فایل .env
load_dotenv()

# اطلاعات اتصال به دیتابیس از متغیر محیطی DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# ساخت Engine: مسئول ارتباط با دیتابیس
engine = create_engine(DATABASE_URL)

# ساخت SessionLocal: هر SessionLocal یک Session برای تعامل با دیتابیس است
# autocommit=False: یعنی تغییرات به صورت خودکار ذخیره نمی‌شوند، باید commit کنیم
# autoflush=False: یعنی تغییرات به صورت خودکار به دیتابیس ارسال نمی‌شوند
# bind=engine: این Session رو به Engine متصل می‌کند
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: این شیء پایه‌ای است که مدل‌های SQLAlchemy از آن ارث می‌برند
Base = declarative_base()

# Dependency برای FastAPI: این تابع یک Session دیتابیس را برای هر درخواست فراهم می‌کند
def get_db():
    db = SessionLocal()
    try:
        yield db # Session را فراهم می‌کند
    finally:
        db.close() # مطمئن می‌شود که Session بسته شود