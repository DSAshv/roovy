from app import db
from models import Album, Song, SongContent
from util import get_uid, generate_unique_string, formatDate


def addAlbumToDB(request):
    try:
        new_album = Album(
            album_id=generate_unique_string(),
            name=request.form.get("name"),
            genre=request.form.get("genre"),
            artist=request.form.get("artist"),
            thumbnail_path=request.form.get("thumbnail_path"),
            status='live',
            created_by=get_uid(),
            created_on=formatDate(request.form.get("created_on"))
        )
        db.session.add(new_album)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def addSongToDB(request):
    song_id = generate_unique_string()
    name = request.form.get('name')
    created_on = formatDate(request.form.get('created_on'))
    status = request.form.get('status')
    album_id = request.form.get('album_id')
    thumbnail_path = request.form.get('thumbnail_path')
    song_type = request.form.get('type')
    content_path = request.form.get('content_path')

    if not (name and created_on and status and album_id and thumbnail_path and song_type and content_path):
        return False, {"error": "missing parameter"}
    try:
        new_song = Song(
            song_id=song_id,
            name=name,
            created_on=created_on,
            status=status,
            album_id=album_id,
            thumbnail_path=thumbnail_path,
            created_by=get_uid()
        )

        new_content = SongContent(
            song_id=song_id,
            type=song_type,
            content_path=content_path
        )

        new_song.content = new_content
        db.session.add(new_song)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False


def editSongInDB(request, song):
    song.name = request.form.get('name')
    song.created_on = request.form.get('created_on')
    song.status = request.form.get('status')
    song.album_id = request.form.get('album_id')
    song.thumbnail_path = request.form.get('thumbnail_path')
    song.content.type = request.form.get('type')
    song.content.content_path = request.form.get('content_path')

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def editAlbum(request, album):
    album.name = request.form.get('name')
    album.genre = request.form.get('genre')
    album.artist = request.form.get('artist')
    album.thumbnail_path = request.form.get('thumbnail_path')
    album.status = request.form.get('status')

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def get_songs_by_user():
    user_id = get_uid()
    if user_id is not None:
        songs_by_user = (
            db.session.query(Song)
            .filter(Song.created_by == user_id)
            .order_by(Song.created_on.desc())
            .all()
        )
        all_songs = []
        for song in songs_by_user:
            song_dict = {
                "song_id": song.song_id,
                "name": song.name,
                "created_on": song.created_on,
                "status": song.status,
                "album_id": song.album_id,
                "thumbnail_path": song.thumbnail_path,
            }
            all_songs.append(song_dict)

        all_songs_tuple = tuple(all_songs)
        return all_songs_tuple
    else:
        return []


def get_albums_by_user():
    user_id = get_uid()
    if user_id is not None:
        all_albums = (
            db.session.query(Album)
            .filter(Album.created_by == user_id)
            .order_by(Album.created_on.desc())
            .all()
        )
        albums_list = []
        for album in all_albums:
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

    else:
        return []
