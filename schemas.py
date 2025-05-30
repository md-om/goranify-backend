# goranify-backend/schemas.py

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime, date


# --- Schemas Base (برای فیلدهای مشترک در Create و Response) ---
class AdvertisementBase(BaseModel):
    title: str
    link: HttpUrl # HttpUrl برای اعتبار سنجی فرمت URL
    cover_url: Optional[HttpUrl] = None
    sponsor: Optional[str] = None


class ArtistBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None # تاریخ تولد
    is_alive: bool = True
    death_date: Optional[date] = None # فقط در صورت is_alive = False
    biography: Optional[str] = None


class AlbumBase(BaseModel):
    title: str
    cover_url: Optional[HttpUrl] = None
    release_year: Optional[int] = None # سال انتشار
    artist_id: int # شناسه خواننده مرتبط


class GenreBase(BaseModel):
    name: str


class MusicBase(BaseModel):
    title: str
    album_id: Optional[int] = None # شناسه آلبوم مرتبط (ممکن است آهنگ آلبوم نداشته باشد)
    artist_id: int # شناسه خواننده مرتبط (هر آهنگ باید یک خواننده داشته باشد)
    cover_url: Optional[HttpUrl] = None
    genre_id: Optional[int] = None # شناسه ژانر مرتبط
    audio_128_url: HttpUrl
    audio_320_url: HttpUrl
    lyrics: Optional[str] = None


# --- Schemas Create (برای داده‌های ورودی هنگام ایجاد رکورد جدید) ---
class AdvertisementCreate(AdvertisementBase):
    pass


class ArtistCreate(ArtistBase):
    pass


class AlbumCreate(AlbumBase):
    pass


class GenreCreate(GenreBase):
    pass


class MusicCreate(MusicBase):
    pass


# --- Schemas Response (برای فرمت داده‌های خروجی API، شامل ID و روابط) ---

# Forward References برای حل مشکل circular import در Pydantic
# وقتی یک مدل به مدل دیگری که هنوز تعریف نشده اشاره می‌کند.
class Album(AlbumBase):
    id: int
    # artist: 'Artist' # این مورد در نهایت در Artist schema تعریف می شود
    musics: List['Music'] = [] # لیست آهنگ‌های مرتبط با آلبوم

    class Config:
        from_attributes = True # یا orm_mode = True در Pydantic v1

# برای Artist
class Artist(ArtistBase):
    id: int
    albums: List[Album] = [] # لیست آلبوم‌های مرتبط با خواننده
    musics: List['Music'] = [] # لیست آهنگ‌های مرتبط با خواننده (برای سهولت دسترسی)

    class Config:
        from_attributes = True

# برای Genre
class Genre(GenreBase):
    id: int
    musics: List['Music'] = [] # لیست آهنگ‌های مرتبط با ژانر

    class Config:
        from_attributes = True

# برای Music
class Music(MusicBase):
    id: int
    # album: Optional[Album] # این مورد در نهایت در Album schema تعریف می شود
    artist: Artist # خواننده مرتبط (فیلد اصلی)
    genre: Optional[Genre] = None # ژانر مرتبط

    class Config:
        from_attributes = True

# اصلاح روابط (برای جلوگیری از خطای Pydantic):
# باید Pydantic را از وجود ForwardRef ها آگاه کنیم.
# این خطوط باید بعد از تعریف تمامی کلاس‌های Schema باشند.
# این کار کمک می‌کند Pydantic بتواند روابط چرخشی (circular dependencies) را حل کند.
Album.model_rebuild()
Artist.model_rebuild()
Music.model_rebuild()

class Advertisement(AdvertisementBase):
    id: int

    class Config:
        from_attributes = True