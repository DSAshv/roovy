from sqlalchemy import Column, String, Enum, ForeignKey, Date, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app import db, app

Base = db.Model


class User(Base):
    __tablename__ = 'USER'

    user_id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum('admin', 'creator', 'user', name='role_enum'), nullable=False)
    status = Column(Enum('flagged', 'blocked', 'live', name='status_enum'))
    __table_args__ = (UniqueConstraint('email', 'role'),)


class UserCredentials(Base):
    __tablename__ = 'USER_CREDENTIALS'

    user_id = Column(String, ForeignKey('USER.user_id'), primary_key=True)
    password = Column(String, primary_key=True)

    user = relationship("User", back_populates="credentials")


User.credentials = relationship("UserCredentials", back_populates="user")


class Song(Base):
    __tablename__ = 'SONG'

    song_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    status = Column(Enum('flagged', 'blocked', 'live', name='status_enum'))
    album_id = Column(String, ForeignKey('ALBUM.album_id'))
    thumbnail_path = Column(String, nullable=False)
    created_by = Column(String, nullable=False)

    album = relationship("Album", back_populates="songs")


class SongContent(Base):
    __tablename__ = 'SONG_CONTENT'

    song_id = Column(String, ForeignKey('SONG.song_id'), primary_key=True)
    type = Column(Enum('song', 'lyric', name='type_enum'))
    content_path = Column(String)

    song = relationship("Song", back_populates="content")


Song.content = relationship("SongContent", back_populates="song", uselist=False)


class Rating(Base):
    __tablename__ = 'RATING'

    song_id = Column(String, ForeignKey('SONG.song_id'), primary_key=True)
    rating = Column(Float, nullable=False)

    song = relationship("Song", back_populates="ratings")


Song.ratings = relationship("Rating", back_populates="song")

class Album(Base):
    __tablename__ = 'ALBUM'

    album_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    thumbnail_path = Column(String, nullable=False)
    status = Column(Enum('flagged', 'blocked', 'live', name='status_enum'))
    created_by = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)

    songs = relationship("Song", back_populates="album")
class Playlist(Base):
    __tablename__ = 'PLAYLIST'

    playlist_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('USER.user_id'), nullable=False)
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="playlists")


User.playlists = relationship("Playlist", back_populates="user")


class SongsInPlaylist(Base):
    __tablename__ = 'SONGS_IN_PLAYLIST'

    playlist_id = Column(String, ForeignKey('PLAYLIST.playlist_id'), primary_key=True)
    song_id = Column(String, ForeignKey('SONG.song_id'), primary_key=True)

    song = relationship("Song", back_populates="playlists")
    playlist = relationship("Playlist", back_populates="songs")


Playlist.songs = relationship("SongsInPlaylist", back_populates="playlist")
Song.playlists = relationship("SongsInPlaylist", back_populates="song")

with app.app_context():
    db.create_all()
