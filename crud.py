# goranify-backend/crud.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_ # برای جستجو
import models, schemas # ایمپورت کردن ماژول‌ها به صورت absolute


# --- توابع CRUD برای Advertisement ---
def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate):
    db_advertisement = models.Advertisement(**advertisement.model_dump())
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

def get_advertisement(db: Session, advertisement_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()

def get_advertisements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Advertisement).offset(skip).limit(limit).all()

def update_advertisement(db: Session, advertisement_id: int, advertisement: schemas.AdvertisementCreate):
    db_advertisement = get_advertisement(db, advertisement_id)
    if db_advertisement:
        for key, value in advertisement.model_dump(exclude_unset=True).items():
            setattr(db_advertisement, key, value)
        db.commit()
        db.refresh(db_advertisement)
        return db_advertisement
    return None

def delete_advertisement(db: Session, advertisement_id: int):
    db_advertisement = get_advertisement(db, advertisement_id)
    if db_advertisement:
        db.delete(db_advertisement)
        db.commit()
        return {"message": "Advertisement deleted successfully"}
    return None


# --- توابع CRUD برای Artist ---
def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artist(db: Session, artist_id: int):
    # از joinedload استفاده می‌کنیم تا آلبوم‌ها و موزیک‌های مرتبط با خواننده هم لود شوند
    return db.query(models.Artist).options(
        joinedload(models.Artist.albums),
        joinedload(models.Artist.musics)
    ).filter(models.Artist.id == artist_id).first()

def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def update_artist(db: Session, artist_id: int, artist: schemas.ArtistCreate):
    db_artist = get_artist(db, artist_id)
    if db_artist:
        for key, value in artist.model_dump(exclude_unset=True).items():
            setattr(db_artist, key, value)
        db.commit()
        db.refresh(db_artist)
        return db_artist
    return None

def delete_artist(db: Session, artist_id: int):
    db_artist = get_artist(db, artist_id)
    if db_artist:
        db.delete(db_artist)
        db.commit()
        return {"message": "Artist deleted successfully"}
    return None


# --- توابع CRUD برای Album ---
def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(**album.model_dump())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def get_album(db: Session, album_id: int):
    # از joinedload برای لود کردن خواننده مرتبط و موزیک‌های آلبوم استفاده می‌کنیم
    return db.query(models.Album).options(
        joinedload(models.Album.artist),
        joinedload(models.Album.musics)
    ).filter(models.Album.id == album_id).first()

def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).offset(skip).limit(limit).all()

def update_album(db: Session, album_id: int, album: schemas.AlbumCreate):
    db_album = get_album(db, album_id)
    if db_album:
        for key, value in album.model_dump(exclude_unset=True).items():
            setattr(db_album, key, value)
        db.commit()
        db.refresh(db_album)
        return db_album
    return None

def delete_album(db: Session, album_id: int):
    db_album = get_album(db, album_id)
    if db_album:
        db.delete(db_album)
        db.commit()
        return {"message": "Album deleted successfully"}
    return None


# --- توابع CRUD برای Genre ---
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genre(db: Session, genre_id: int):
    # از joinedload برای لود کردن موزیک‌های مرتبط با ژانر استفاده می‌کنیم
    return db.query(models.Genre).options(
        joinedload(models.Genre.musics)
    ).filter(models.Genre.id == genre_id).first()

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def update_genre(db: Session, genre_id: int, genre: schemas.GenreCreate):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        for key, value in genre.model_dump(exclude_unset=True).items():
            setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    return None

def delete_genre(db: Session, genre_id: int):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db.delete(db_genre)
        db.commit()
        return {"message": "Genre deleted successfully"}
    return None


# --- توابع CRUD برای Music ---
def create_music(db: Session, music: schemas.MusicCreate):
    db_music = models.Music(**music.model_dump())
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music

def get_music(db: Session, music_id: int):
    # از joinedload برای لود کردن اطلاعات آلبوم، خواننده و ژانر مرتبط با موزیک استفاده می‌کنیم
    return db.query(models.Music).options(
        joinedload(models.Music.album),
        joinedload(models.Music.artist),
        joinedload(models.Music.genre)
    ).filter(models.Music.id == music_id).first()

def get_musics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Music).offset(skip).limit(limit).all()

def search_musics(db: Session, query: str, skip: int = 0, limit: int = 100):
    search_pattern = f"%{query.lower()}%"
    return (
        db.query(models.Music)
        .filter(
            or_(
                models.Music.title.ilike(search_pattern),
                # برای جستجو در خواننده، باید مطمئن شویم که Artist لود شده و full_name وجود دارد
                models.Music.artist.has(models.Artist.full_name.ilike(search_pattern)),
                models.Music.album.has(models.Album.title.ilike(search_pattern)) # جستجو در عنوان آلبوم
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_music(db: Session, music_id: int, music: schemas.MusicCreate):
    db_music = get_music(db, music_id)
    if db_music:
        for key, value in music.model_dump(exclude_unset=True).items():
            setattr(db_music, key, value)
        db.commit()
        db.refresh(db_music)
        return db_music
    return None

def delete_music(db: Session, music_id: int):
    db_music = get_music(db, music_id)
    if db_music:
        db.delete(db_music)
        db.commit()
        return {"message": "Music deleted successfully"}
    return None