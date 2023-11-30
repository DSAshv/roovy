import uuid
from datetime import datetime

from flask import session
from sqlalchemy import func

from app import db
from models import Song, Album, Playlist, User, SongsInPlaylist


def generate_unique_string():
    unique_string = str(uuid.uuid4())
    return unique_string


def get_uid():
    return session.get("uid")


def getSongFromId(song_id):
    return Song.query.get(song_id)


def getAlbumFromId(album_id):
    return Album.query.get(album_id)


def getPlaylistFromId(playlist_id):
    return Playlist.query.get(playlist_id)
def formatDate(created_on_str):
    return datetime.fromisoformat(created_on_str)


def getPlaylistsForUser():
    try:
        user_playlists = (
            db.session.query(Playlist)
            .join(User, Playlist.user_id == User.user_id)
            .filter(User.user_id == get_uid())
            .all()
        )

        playlists_list = []
        for playlist in user_playlists:
            playlist_details = {
                "playlist_id": playlist.playlist_id,
                "name": playlist.name
            }
            playlists_list.append(playlist_details)

        return playlists_list

    except Exception as e:
        print(f"Error fetching playlists for user: {e}")
        return []


def getAlbumsForUser():
    try:
        user_albums = (
            db.session.query(Album)
            .filter(Album.created_by == get_uid())
            .all()
        )

        albums_list = []
        for album in user_albums:
            album_details = {
                "album_id": album.album_id,
                "name": album.name,
                "genre": album.genre,
                "artist": album.artist,
                "thumbnail_path": album.thumbnail_path,
                "status": album.status,
            }
            albums_list.append(album_details)

        return albums_list

    except Exception as e:
        print(f"Error fetching albums for user: {e}")
        return []


def getNameFromId():
    return User.query.get(get_uid()).name


def getNoOfSongsInAlbum(album_id):
    try:
        num_songs = (
            db.session.query(func.count(Song.song_id))
            .filter(Song.album_id == album_id)
            .scalar()
        )
        return num_songs
    except Exception as e:
        return "No data available"


def getNoOfSongsInPlaylist(playlist_id):
    try:
        num_songs = (
            db.session.query(func.count(SongsInPlaylist.song_id))
            .filter(SongsInPlaylist.playlist_id == playlist_id)
            .scalar()
        )
        return num_songs
    except Exception as e:
        return "No data available"
