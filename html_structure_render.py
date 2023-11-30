from flask import url_for
from app import db
from creator_module import getAvgRating
from models import Song, Album, Playlist, User

from util import getPlaylistsForUser, get_uid, getAlbumFromId, getNoOfSongsInAlbum, getNoOfSongsInPlaylist


def get_all_songs():
    songs_with_details = (
        db.session.query(Song, Album)
        .join(Album, Song.album_id == Album.album_id)
        .order_by(Song.created_on.desc())
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

def generate_song_html_structure(song_details, editable):
    user_playlists_dropdown_options = getUserPlaylistsDropdownOptions()
    edit_button = f'''<a class="editBtn" href="../edit_song/{song_details['song_id']}">Edit</a>
    <form id="deleteSongForm" action="/delete_song/{song_details['song_id']}" method="POST">
    <button type="submit">Delete</button>
    </form>''' if editable else ''

    html_structure = f"""
        <div class="song">
            <div class="songThumbnail">
                <img src="{song_details['thumbnail_path']}" alt="Thumbnail">
            </div>
            <div class="songDetails">
                <div class="songName">
                    <p>{song_details['name']}</p>
                    <p>Album: {getAlbumFromId(song_details['album_id']).name}</p>
                </div>
                <div class="songInfo">
                        <p>Artist: {song_details['artist_name']}</p>
                        <p>Genre: {song_details['genre']}</p>
                        <p>Ratings: {getAvgRating(song_details['song_id'])}</p>
                        <div id="rating">
                            <form method="POST" action="/add_rating">
                                <input type="hidden" name="song_id" value="{song_details['song_id']}">                    
                                <select id="rating" name="rating" required>
                                    <option value="5">5</option>
                                    <option value="4">4</option>
                                    <option value="3">3</option>
                                    <option value="2">2</option>
                                    <option value="1">1</option>
                                </select>
                                <button type="submit">Rate</button>
                            </form>
                        </div>
                </div>
            </div>
            <div class="songActions">
                <div class="addToPlaylistForm">
                    <form method="POST" action="/add_to_playlist">
                        <input type="hidden" name="song_id" value="{song_details['song_id']}">
                        <select name="playlist_id">
                            {user_playlists_dropdown_options}
                        </select>
                        <button type="submit">Add to Playlist</button>
                    </form>
                </div>
                <button class="playBtn" onclick="playSong('{song_details['song_id']}')">Play</button>
            </div>
            {edit_button}
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
                <p>No. of songs: {getNoOfSongsInAlbum(album['album_id'])}</p>
                <!-- Add more details as needed -->
                <a href="../album/{album['album_id']}">View Album</a>
                {'<a href="../edit_album/' + album['album_id'] + '">Edit Album</a><form id="deleteAlbumForm" action="/delete_album/' + album['album_id'] + '" method="POST"><button type="submit">Delete Album</button></form>' if editable else ''}
            </div>
        </div>
    """
    return html_structure


def get_all_playlists():
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
            <h4>No. of songs : {getNoOfSongsInPlaylist(playlist['playlist_id'])}</h4>
            <a href="../playlist/{playlist['playlist_id']}">View Playlist</a>
            <form id="deletePlaylistForm" action="{url_for('delete_playlist', playlist_id=playlist['playlist_id'])}" method="POST">
                <button type="submit">Delete Playlist</button>
            </form>
        </div>
    """


def album_and_song_content(album_id):
    try:
        album = db.session.query(Album).filter_by(album_id=album_id).first()

        if album:
            user_playlists_dropdown_options = getUserPlaylistsDropdownOptions()
            songs_in_album = album.songs
            song_html_list = ""

            for song in songs_in_album:
                song_html_list += (
                    f"""
                    <div class="song">
                        <div class="songThumbnail">
                            <img src="../{song.thumbnail_path}" alt="Thumbnail">
                        </div>
                        <div class="songDetails">
                            <div class="songName">{song.name}</div>
                        </div>    
                        <div class="addToPlaylistForm">
                            <form method="POST" action="/add_to_playlist>
                                <input type="hidden" name="song_id" value="{song.song_id}">
                                    <select name="playlist_id">
                                        {user_playlists_dropdown_options}
                                    </select>
                                <button type="submit">Add to Playlist</button>                            
                            </form>
                        </div>    
                        <button class="playBtn" onclick="playSong('{song.song_id}')">Play</button>
                    </div>
                """).replace("\n", "")

            return song_html_list
        else:
            return "Album not found", 404

    except Exception as e:
        print(f"Error rendering album and song content: {e}")
        return "Internal Server Error", 500


def playlist_and_song_content(playlist_id):
    try:
        playlist = db.session.query(Playlist).filter_by(playlist_id=playlist_id).first()

        if playlist:
            songs_in_playlist = playlist.songs
            song_html_list = ""
            user_playlists_dropdown_options = getUserPlaylistsDropdownOptions()

            for song in songs_in_playlist:
                song_html_list += (
                    f"""
                    <div class="song">
                        <div class="songThumbnail">
                            <img src="../{song.song.thumbnail_path}" alt="Thumbnail">
                        </div>
                        <div class="songDetails">
                            <div class="songName">{song.song.name}</div>
                        </div>
                        <div class="addToPlaylistForm">
                            <form method="POST" action="/add_to_playlist">
                                <input type="hidden" name="song_id" value="{song.song.song_id}">
                                <select name="playlist_id">
                                    {user_playlists_dropdown_options}
                                </select>
                                <button type="submit">Add to Playlist</button>
                            </form>
                        </div>
                        <button class="playBtn" onclick="playSong('{song.song.song_id}')">Play</button>
                    </div>
                """
                ).replace("\n", "")

            return song_html_list
        else:
            return "Album not found", 404

    except Exception as e:
        print(f"Error rendering album and song content: {e}")
        return "Internal Server Error", 500


def getUserPlaylistsDropdownOptions():
    user_playlists = getPlaylistsForUser()
    options = ""
    for playlist in user_playlists:
        options += f"<option value='{playlist['playlist_id']}'>{playlist['name']}</option>"
    return options
