from sqlalchemy.orm import joinedload, aliased
from models import Album, SongContent, Rating
from util import get_uid, generate_unique_string, formatDate, getNameFromId


def addAlbumToDB(request):
    try:
        new_album = Album(
            album_id=generate_unique_string(),
            name=request.form.get("name"),
            genre=request.form.get("genre"),
            artist=getNameFromId(),
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
    song.created_on = formatDate(request.form.get('created_on'))
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


def editAlbumInDB(request, album):
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
    songs_with_details = (
        db.session.query(Song, Album)
        .outerjoin(Rating, Song.song_id == Rating.song_id)
        .options(joinedload(Song.ratings))
        .join(Album, Song.album_id == Album.album_id)
        .order_by(Song.created_on.desc())
        .filter(Song.created_by == get_uid())
        .all()
    )

    all_songs = []
    for song, album in songs_with_details:
        song_dict = {
            "song_id": song.song_id,
            "name": song.name,
            "created_on": song.created_on,
            "status": song.status,
            "album_id": song.album_id,
            "thumbnail_path": song.thumbnail_path,
            "ratings": [rating.rating for rating in song.ratings] if song.ratings else [0],
            "album_name": album.name,
            "artist_name": album.artist,
            "genre": album.genre
        }
        all_songs.append(song_dict)

    all_songs_tuple = tuple(all_songs)
    return all_songs_tuple


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


def addPlaylist(name):
    try:
        user_id = get_uid()
        if user_id is not None:
            new_playlist = Playlist(
                playlist_id=generate_unique_string(),
                user_id=user_id,
                name=name
            )
            db.session.add(new_playlist)
            db.session.commit()
            return True
        else:
            return False

    except Exception as e:
        print(f"Error adding playlist: {e}")
        return False


from models import db, SongsInPlaylist, Song, Playlist


def addSongToPlaylist(song_id, playlist_id):
    try:
        song = db.session.query(Song).filter_by(song_id=song_id).first()
        playlist = db.session.query(Playlist).filter_by(playlist_id=playlist_id).first()

        if song and playlist:
            if not db.session.query(SongsInPlaylist).filter_by(song_id=song_id, playlist_id=playlist_id).first():
                songs_in_playlist = SongsInPlaylist(song_id=song_id, playlist_id=playlist_id)
                db.session.add(songs_in_playlist)
                db.session.commit()
                return True, "Song added to playlist successfully"
            else:
                return False, "Song is already in the playlist"
        else:
            return False, "Song or playlist not found"

    except Exception as e:
        print(f"Error adding song to playlist: {e}")
        db.session.rollback()
        return False, "Internal Server Error"


def deleteAlbum(album_id):
    try:
        album = db.session.query(Album).filter_by(album_id=album_id)

        if album:
            db.session.delete(album)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        return False


def deleteSong(song_id):
    try:
        song = db.session.query(Song).filter_by(song_id=song_id).first()

        if song:
            db.session.delete(song)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        return False


def deletePlaylist(playlist_id):
    try:
        playlist = Playlist.query.get(playlist_id)
        delete_statement = SongsInPlaylist.__table__.delete().where(SongsInPlaylist.playlist_id == playlist_id)
        db.session.execute(delete_statement)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
        else:
            return False

    except Exception as e:
        return False

    return True


def addRating(song_id, score):
    try:
        rating = Rating.query.get(song_id)
        if rating is None:
            new_rating = Rating(song_id=song_id, count=1, rating=score)
            db.session.add(new_rating)
        else:
            rating.count += 1
            rating.rating += float(score)

        db.session.commit()
        return True

    except Exception as e:
        return False


def getAvgRating(song_id):
    rating = Rating.query.get(song_id)
    if rating == None:
        return "0"
    return rating.rating / rating.count


def playSong(song_id):
    toReturn = ""
    data = get_songs_with_content_and_album(song_id)
    if (data[1].type == "song"):
        html_content = f"""
        <div class="songDetails">
            <h2>{data[0].name}</h2>
            <p>Album: {data[2].name}</p>
            <p>Genre: {data[2].genre}</p>
            <p>Artist: {data[2].artist}</p>
        </div>
        """
        toReturn += generate_player_content_template(html_content, data[0].thumbnail_path)
    else:
        with open(data[1].content_path, 'r') as file:
            file_content = file.read()
        toReturn += generate_player_content_template(f'<div>{file_content}</div>', data[0].thumbnail_path)

    return [data[1].content_path, toReturn]


def get_songs_with_content_and_album(song_id):
    try:
        song_alias = aliased(Song)
        content_alias = aliased(SongContent)
        album_alias = aliased(Album)

        songs_data = (
            db.session.query(song_alias, content_alias, album_alias)
            .join(content_alias, song_alias.song_id == content_alias.song_id)
            .join(album_alias, song_alias.album_id == album_alias.album_id)
            .filter(song_alias.song_id == song_id)
        )

        return songs_data[0]

    except Exception as e:
        return []


def generate_player_content_template(song_content, thumbnail_path):
    return f"""
    <div id="playerContentThumbnail">
        <img src="{thumbnail_path}" alt="Thumbnail">
    </div>

    <div id="playerActualContent">
        {song_content}
    </div>
    """
