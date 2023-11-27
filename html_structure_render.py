from sqlalchemy import func

from app import db
from models import Song, Rating, Album, Playlist
from sqlalchemy.orm import joinedload


def get_all_songs():
    songs_with_ratings = (
        db.session.query(
            Song,
            func.coalesce(func.avg(Rating.rating), 0).label("average_rating")
        )
        .outerjoin(Rating, Song.song_id == Rating.song_id)
        .group_by(Song.song_id)
        .options(joinedload(Song.ratings))
        .order_by(Song.created_on.desc())
        .all()
    )

    all_songs = []
    for song in songs_with_ratings:
        song = song[0]
        song_dict = {
            "song_id": song.song_id,
            "name": song.name,
            "created_on": song.created_on,
            "status": song.status,
            "album_id": song.album_id,
            "thumbnail_path": song.thumbnail_path,
            "ratings": [rating.rating for rating in song.ratings] if song.ratings else [],
        }
        all_songs.append(song_dict)

    all_songs_tuple = tuple(all_songs)
    return all_songs_tuple


def generate_song_html_structure(song_details, editable):
    edit_button = f'<button class="editBtn" onclick="editSong(\'{song_details["song_id"]}\')">Edit</button>' if editable else ''

    html_structure = f"""
        <div class="song">
            <div class="songThumbnail">
                <img src="{song_details['thumbnail_path']}" alt="Thumbnail">
            </div>
            <div class="songDetails">
                <div class="songName">{song_details['name']}</div>
                <div class="songInfo">
                    <p>Created On: {song_details['created_on']}</p>
                    <p>Status: {song_details['status']}</p>
                    <p>Album Name: {song_details['album_id']}</p>
                </div>
            </div>
            <div class="songActions">
                <button class="playBtn" onclick="playSong('{song_details['song_id']}')">Play</button>
                {edit_button}
            </div>
        </div>
    """
    return html_structure


def get_all_albums():
    try:
        all_albums = db.session.query(Album).all()
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

    except Exception as e:
        print(f"Error fetching albums: {e}")
        return []


def generate_album_html_structure(album, editable):
    html_structure = f"""
        <div class="album">
            <img src="{album['thumbnail_path']}" alt="{album['name']} Thumbnail">
            <div class="albumDetails">
                <h2>{album['name']}</h2>
                <p>Genre: {album['genre']}</p>
                <p>Artist: {album['artist']}</p>
                <p>Status: {album['status']}</p>
                <!-- Add more details as needed -->
                <a href="../album/{album['album_id']}">View Album</a>
                {'<button onclick="editAlbum("' + album['album_id'] + ')">Edit Album</button>' if editable else ''}
            </div>
        </div>
    """
    return html_structure


def get_all_playlists():
    try:
        all_playlists = db.session.query(Playlist).all()
        playlists_list = []
        for playlist in all_playlists:
            playlist_details = {
                "playlist_id": playlist.playlist_id,
                "user_id": playlist.user_id,
                "name": playlist.name,
            }
            playlists_list.append(playlist_details)

        return playlists_list

    except Exception as e:
        print(f"Error fetching playlists: {e}")
        return []


def generate_playlist_html_structure(playlist):
    return f"""
        <div class="playlist">
            <h2>{playlist['name']}</h2>
            <p>User ID: {playlist['user_id']}</p>
            <!-- Add more details as needed -->
            <a href="../playlist/{playlist['playlist_id']}">View Playlist</a>
        </div>
    """
