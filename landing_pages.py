from flask import render_template

from app import db
from creator_module import get_songs_by_user, get_albums_by_user
from html_structure_render import get_all_songs, get_all_albums, generate_song_html_structure, \
    generate_album_html_structure, get_all_playlists, generate_playlist_html_structure
from models import Album
from util import get_uid, getSongToEdit

nav_elements = ()


def setNavElems(elems):
    global nav_elements
    nav_elements = elems


def userLandingPage(content="songs"):
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

def adminLandingPage():
    return "admin page"


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
        song = getSongToEdit(request.path.song_id)
        return edit_song(song)


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
    header_left = "> Playlists"
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
    html = ""
    for playlist_details in all_playlist_tuple:
        html += generate_playlist_html_structure(playlist_details)
    return html


def edit_song(song):
    header_left = "> Edit song"
    content = render_template('edit_song.html', song)
    current_song = "Now Playing: None"
    return render_template('parent_frame.html', content=content, current_song=current_song, header_left=header_left,
                           nav_elements=nav_elements)
