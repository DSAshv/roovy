from flask import render_template, url_for

import account_module
from app import db
from users_module import get_songs_by_user, get_albums_by_user
from html_structure_render import get_all_songs, get_all_albums, generate_song_html_structure, \
    generate_album_html_structure, get_all_playlists, generate_playlist_html_structure, album_and_song_content, \
    playlist_and_song_content, overview_html
from models import Album
from util import get_uid, getSongFromId, getAlbumFromId, getPlaylistFromId, getAlbumsForUser

nav_elements = ()
def setNavElems(elems):
    global nav_elements
    nav_elements = elems


def adminLandingPage(content='Overview'):
    setNavElems((
        {'title': 'Overview', 'url': '../admin-overview', 'class': 'first'},
        {'title': 'Accounts', 'url': '../accounts', },
        {'title': 'Songs', 'url': '../admin-songs'},
    ))
    if content == "Accounts":
        header_left = "> Accounts Overview"
        content = render_template("dashboard_accounts.html", users=account_module.getAllUsers())
        current_song = ""
        return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                               nav_elements=nav_elements)
    elif content == "Songs":
        header_left = "> Songs Overview"
        content = render_template("dashboard_songs.html", all_songs=get_all_songs())
        current_song = ""
        return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                               nav_elements=nav_elements)
    elif content == "Overview":
        header_left = ">Overview"
        content = overview_html()
        current_song = ""
        return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                               nav_elements=nav_elements)


def userLandingPage(content="songs", request=None):
    setNavElems((
        {'title': 'Songs', 'url': '../songs', 'class': 'first'},
        {'title': 'Albums', 'url': '../albums'},
        {'title': 'My Playlists', 'url': '../playlists'},
        {'title': 'Are you a creator?', 'url': '../creator', 'class': 'creatorInNav'}
    ))
    if content == "songs":
        return getSongs()
    elif content == "albums":
        return getAlbums()
    elif content == "playlists":
        return getPlaylists()
    elif content == "getModuleContent":
        module, id = request.path.split("/")[1:]
        if module == "album":
            return getAlbumAndSongs(id)
        elif module == "playlist":
            return getPlaylistAndSongs(id)
    elif content == "search":
        return returnSearchPage(request)

def creatorLandingPage(content="songs", request=None):
    setNavElems((
        {'title': 'Songs', 'url': '../songs', 'is_first': True},
        {'title': 'Albums', 'url': '../albums'},
        {'title': 'My Playlists', 'url': '../playlists'},
        {'title': 'My Songs', 'url': '../mysongs'},
        {'title': 'My Albums', 'url': '../myalbums'},
        {'title': 'Add Songs', 'url': '../create_song'},
        {'title': 'Add Albums', 'url': '../create_album'}
    ))

    if content == "songs":
        return getSongs()
    elif content == "albums":
        return getAlbums()
    elif content == "playlists":
        return getPlaylists()
    elif content == "mysongs":
        return getMySongs()
    elif content == "myalbums":
        return getMyAlbums()
    elif content == "create_song":
        album_choices = [(album.album_id, album.name) for album in
                         db.session.query(Album).filter(Album.created_by == get_uid()).all()]
        return create_song(album_choices)
    elif content == "create_album":
        return create_album()
    elif content == "edit_song":
        song = getSongFromId(request.path.split("/")[-1])
        return edit_song(song)
    elif content == "edit_album":
        album = getAlbumFromId(request.path.split("/")[-1])
        return edit_album(album)
    elif content == "getModuleContent":
        module, id = request.path.split("/")[1:]
        if module == "album":
            return getAlbumAndSongs(id)
        elif module == "playlist":
            return getPlaylistAndSongs(id)
    elif content == "search":
        return returnSearchPage(request)


def getSongs():
    header_left = "> Songs"
    content = render_songs_content()
    current_song = "Now Playing: Song Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def getMySongs():
    header_left = "> My songs"
    content = render_my_songs_content()
    current_song = "Now Playing: Song Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def getAlbums():
    header_left = "> My Albums"
    content = render_albums_content()
    current_song = "Now Playing: Album Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def getMyAlbums():
    header_left = "> My Albums"
    content = render_my_albums_content()
    current_song = "Now Playing: Album Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def getPlaylists():
    header_left = "> Playlist"
    content = render_playlist_content()
    current_song = "Now Playing: Album Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def create_song(album_choices):
    header_left = "> Add new song"
    content = render_template('add_song.html', album_choices=album_choices)
    current_song = "Now Playing: None"
    return render_template('parent_frame.html', content=content, current_song=current_song, header_left=header_left,
                           nav_elements=nav_elements)


def create_album():
    header_left = "> Add new album"
    content = render_template('create_album.html')
    current_song = "Now Playing: None"
    return render_template('parent_frame.html', content=content, current_song=current_song, header_left=header_left,
                           nav_elements=nav_elements)


def render_songs_content():
    all_songs_tuple = get_all_songs()
    html = ""
    for song_details in all_songs_tuple:
        html += generate_song_html_structure(song_details, False)
    return html
def render_my_songs_content():
    all_songs_tuple = get_songs_by_user()
    html = ""
    for song_details in all_songs_tuple:
        html += generate_song_html_structure(song_details, True)
    return html


def render_albums_content():
    all_albums_tuple = get_all_albums()
    html = ""
    for album_details in all_albums_tuple:
        html += generate_album_html_structure(album_details, False)
    return html


def render_my_albums_content():
    all_album_tuple = get_albums_by_user()
    html = ""
    for album_details in all_album_tuple:
        html += generate_album_html_structure(album_details, True)
    return html


def render_playlist_content():
    all_playlist_tuple = get_all_playlists()
    html = f"""
    <form id="addPlaylistForm" method="POST" action="{url_for('createPlaylist')}">
        <label for="playlistName">Playlist Name:</label>
        <input type="text" id="playlistName" name="name" required>

        <button type="submit">Create Playlist</button>
    </form>"""

    for playlist_details in all_playlist_tuple:
        html += generate_playlist_html_structure(playlist_details)
    return html


def edit_song(song):
    header_left = "> Edit song"
    album_choices = getAlbumsForUser()
    album_choices = [(album.get("album_id"), album.get("name")) for album in album_choices]
    content = render_template('edit_song.html', song=song, album_choices=album_choices)
    current_song = "Now Playing: None"
    return render_template('parent_frame.html', content=content, current_song=current_song, header_left=header_left,
                           nav_elements=nav_elements)


def edit_album(album):
    header_left = "> Edit album"
    content = render_template('edit_album.html', album=album)
    current_song = "Now Playing: None"
    return render_template('parent_frame.html', content=content, current_song=current_song, header_left=header_left,
                           nav_elements=nav_elements)


def getAlbumAndSongs(id):
    header_left = "> Album > " + getAlbumFromId(id).name
    content = album_and_song_content(id)
    current_song = "Now Playing: Album Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def getPlaylistAndSongs(id):
    header_left = "> Playlist > " + getPlaylistFromId(id).name
    content = playlist_and_song_content(id)
    current_song = "Now Playing: Album Name"
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song=current_song,
                           nav_elements=nav_elements)


def returnSearchPage(details):
    header_left = "> Search Results "
    content = ""
    for song_details in details[0]:
        content += generate_song_html_structure(song_details, False)
    for album_details in details[1]:
        content += generate_album_html_structure(album_details, False)
    return render_template('parent_frame.html', header_left=header_left, content=content, current_song="",
                           nav_elements=nav_elements)
