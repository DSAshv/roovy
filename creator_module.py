from app import db
from models import Album, Song, SongContent


def createAlbum(request):
    try:
        new_album = Album(
            name=request.form.name.data,
            genre=request.form.genre.data,
            artist=request.form.artist.data,
            thumbnail_path=request.form.thumbnail_path.data,
            status='live'
        )
        db.session.add(new_album)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def add_song(request):
    name = request.form.get('name')
    created_on = request.form.get('created_on')
    status = request.form.get('status')
    album_id = request.form.get('album_id')
    thumbnail_path = request.form.get('thumbnail_path')
    song_type = request.form.get('type')
    content_path = request.form.get('content_path')

    if not (name and created_on and status and album_id and thumbnail_path and song_type and content_path):
        return False, {"error": "missing parameter"}
    try:
        new_song = Song(
            name=name,
            created_on=created_on,
            status=status,
            album_id=album_id,
            thumbnail_path=thumbnail_path
        )

        new_content = SongContent(
            type=song_type,
            content_path=content_path
        )

        new_song.content = new_content
        db.session.add(new_song)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False, {"error": e}


def editSong(request, song):
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


def getSongToEdit(song_id):
    return Song.query.get(song_id)


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


def getAlbum(album_id):
    return Album.query.get(album_id)
