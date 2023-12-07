import os

import account_module
import users_module
from landing_pages import userLandingPage, adminLandingPage, creatorLandingPage
from util import generate_unique_string, getSongFromId, getAlbumFromId
from app import app
from flask import render_template, request, flash, session

@app.route("/")
def index():
    if not session.get("uid"):
        return render_template("user_entry.html")
    else:
        if (not account_module.getUserStatus(session.get("uid"))):
            logout()
            return render_template("user_blocked.html")
        if session.get("role") == "user":
            return userLandingPage()
        elif session.get("role") == "admin":
            return adminLandingPage()
        elif session.get("role") == "creator":
            return creatorLandingPage()
        else:
            flash("Undefined role", "error")
            return index(), 400
    return index(), 500

@app.route("/user", methods=["GET"])
@app.route("/creator", methods=["GET"])
@app.route("/admin", methods=["GET"])
def entryPage():
    try:
        if request.path == "/user":
            if session.get("uid") and session.get("role") == 'user':
                return userLandingPage(), 200
            return render_template("user_entry.html"), 200
        elif request.path == "/creator":
            if session.get("uid") and session.get("role") == 'creator':
                return creatorLandingPage(), 200
            return render_template("creator_entry.html"), 200
        elif request.path == "/admin":
            if session.get("uid") and session.get("role") == 'admin':
                return adminLandingPage(), 200
            return render_template("admin_login.html"), 200
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route("/user-sign-in", methods=["POST"])
@app.route("/creator-sign-in", methods=["POST"])
@app.route("/admin-sign-in", methods=["POST"])
def signIn():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if request.path == "/user-sign-in":
            role = "user"
        elif request.path == "/creator-sign-in":
            role = "creator"
        elif request.path == "/admin-sign-in":
            role = "admin"

        authorization, uid, status = account_module.authorizeUser(email, password, role)
        if authorization:
            session["uid"] = uid
            session["role"] = role
            return index()
        else:
            return render_template("error_login.html"), 200
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route("/user-sign-up", methods=["POST"])
@app.route("/creator-sign-up", methods=["POST"])
def signUp():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if request.path == "/user-sign-up":
            role = "user"
        elif request.path == "/creator-sign-up":
            role = "creator"
        else:
            return index(), 400
        uid = generate_unique_string()
        if account_module.signup(uid, email, name, role, password):
            session["uid"] = uid
            session["role"] = role
            return index()
        flash("Signup failed. Please try again with different email.", "error")
        return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route("/logout")
def logout():
    try:
        session.clear()
        return index()
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/create_album', methods=['GET', 'POST'])
def createAlbum():
    try:
        if request.method == 'GET':
            return creatorLandingPage("create_album"), 200

        thumbnail = request.files['thumbnail_path']
        if thumbnail:
            thumbnailname = os.path.join(app.config['THUMBNAIL_UPLOAD_FOLDER'], thumbnail.filename)
            thumbnail.save(thumbnailname)

        if users_module.addAlbumToDB(request, os.path.join('thumbnails', thumbnail.filename)):
            return index()
        else:
            flash("Album creation failed. Please try again.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/create_song', methods=['GET', 'POST'])
def createSong():
    try:
        if request.method == 'GET':
            return creatorLandingPage("create_song"), 200

        file = request.files['content_path']
        thumbnail = request.files['thumbnail_path']
        if file and thumbnail:
            filename = os.path.join(app.config['SONG_UPLOAD_FOLDER'], file.filename)
            thumbnailname = os.path.join(app.config['THUMBNAIL_UPLOAD_FOLDER'], thumbnail.filename)
            file.save(filename)
            thumbnail.save(thumbnailname)
            content_path = os.path.join('songs', file.filename)
            thumbnail_path = os.path.join('thumbnails', thumbnail.filename)

            if users_module.addSongToDB(request, content_path, thumbnail_path):
                return index()
            else:
                flash("Song creation failed. Please try again later.", "error")
                return index(), 500
        else:
            flash("Song creation failed. Upload proper files.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/create_playlist', methods=['POST'])
def createPlaylist():
    try:
        if users_module.addPlaylist(request.form.get("name")):
            request.path = "/playlists"
            return getContent()
        else:
            flash("Playlist creation failed. Please try again.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/edit_song/<string:song_id>', methods=['GET', 'POST'])
def editSong(song_id):
    try:
        if request.method == 'GET':
            return creatorLandingPage("edit_song", request), 200
        if users_module.editSongInDB(request, getSongFromId(song_id)):
            request.path = "/mysongs"
            return getContent()
        else:
            flash("Song editing failed. Please try again.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/edit_album/<string:album_id>', methods=['GET', 'POST'])
def editAlbum(album_id):
    try:
        album = getAlbumFromId(album_id)
        if request.method == 'POST':
            if users_module.editAlbumInDB(request, album):
                flash("Album edited successfully", "success")
                request.path = "/myalbums"
                return getContent()
            else:
                flash("Error editing the album. Please try again.", "error"), 500
        return creatorLandingPage("edit_album", request), 200
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    try:
        user_id = session.get("uid")
        if not user_id:
            flash("Authenticate first", "error")
            return index()

        if request.method == 'POST':
            if account_module.updateProfile(request, user_id):
                flash("Profile updated successfully", "success")
            else:
                flash("Email is already in use. Please choose another one.", "error")

        return render_template('profile.html', user=account_module.getUser(user_id)), 200
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route('/songs', methods=['GET'])
@app.route('/albums', methods=['GET'])
@app.route('/mysongs', methods=['GET'])
@app.route('/myalbums', methods=['GET'])
@app.route('/playlists', methods=['GET'])
def getContent():
    try:
        content = request.path.lstrip("/")
        if session.get("role") == "user":
            return userLandingPage(content), 200
        elif session.get("role") == "creator":
            return creatorLandingPage(content), 200
        else:
            flash("Cannot load content.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route('/album/<string:id>', methods=['GET'])
@app.route('/playlist/<string:id>', methods=['GET'])
def getAlbumDetails(id):
    try:
        content = "getModuleContent"
        if session.get("role") == "user":
            return userLandingPage(content, request), 200
        elif session.get("role") == "creator":
            return creatorLandingPage(content, request), 200
        else:
            flash("Cannot load content.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    try:
        if users_module.addSongToPlaylist(request.form.get("song_id"), request.form.get("playlist_id")):
            request.path = "/playlist/" + request.form.get("playlist_id")
            return getAlbumDetails(request.form.get("playlist_id"))
        else:
            flash("Failed to add to playlist. Please try again.", "error")
            return index(), 500
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/delete_album/<album_id>', methods=['POST'])
def delete_album(album_id):
    try:
        if request.method == 'POST':
            if users_module.deleteAlbum(album_id):
                flash("Album deleted successfully", "success")
                request.path = "/myalbums"
                return getContent()
            else:
                flash("Album not found or error occurred", "error")
                return index(), 404
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/delete_song/<song_id>', methods=['POST'])
def delete_song(song_id):
    try:
        if request.method == 'POST':
            if users_module.deleteSong(song_id):
                flash("Song deleted successfully", "success")
                request.path = "/mysongs"
                return getContent()
            else:
                flash("Song not found or error occurred", "error")
                return index(), 404
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/delete_playlist/<playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    try:
        if request.method == 'POST':
            if users_module.deletePlaylist(playlist_id):
                flash("Playlist deleted successfully", "success")
                request.path = "/playlists"
                return getContent()
            else:
                flash("Playlist not found or error occurred", "error")
                return index(), 404
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/add_rating', methods=['POST'])
def add_rating():
    try:
        if request.method == 'POST' and users_module.addRating(request.form.get("song_id"), request.form.get('rating')):
            flash("Rating added successfully", "success")
            return index(), 200
        else:
            flash("Failed to add rating", "error")
            return index(), 400
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500

@app.route('/play_song/<string:song_id>', methods=['POST'])
def play(song_id):
    try:
        if request.method == 'POST':
            return users_module.playSong(song_id)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return index(), 500


@app.route("/search", methods=["POST"])
def search():
    searchQuery = request.form.get("searchQuery")
    song_details = users_module.searchSongs(searchQuery)
    album_details = users_module.searchAlbums(searchQuery)
    if session.get("role") == 'user':
        return userLandingPage('search', [song_details, album_details])
    else:
        return creatorLandingPage('search', [song_details, album_details])


def is_admin_route(route):
    return route in {'admin_acc_dashboard', 'admin_songs_dashboard', 'admin_dashboard', 'edit_song_status',
                     'edit_acc_status'}


def check_admin_access():
    if request.endpoint and is_admin_route(request.endpoint):
        if (not ('role' not in session or session['role'] != 'admin')):
            return True
    else:
        return False


@app.route("/accounts")
def admin_acc_dashboard():
    if check_admin_access():
        return adminLandingPage("Accounts")
    else:
        return unauthorized()


@app.route("/admin-songs")
def admin_songs_dashboard():
    if check_admin_access():
        return adminLandingPage("Songs")
    else:
        return unauthorized()


@app.route("/admin-overview")
def admin_dashboard():
    if check_admin_access():
        return adminLandingPage("Overview")
    else:
        return unauthorized()


@app.route("/edit_song_status", methods=["POST"])
def edit_song_status():
    if check_admin_access():
        song_id = request.form.get("song_id")
        new_status = request.form.get("new_status")
        account_module.changeSongStatus(song_id, new_status)
        return admin_songs_dashboard()
    else:
        return unauthorized()


@app.route("/edit_acc_status", methods=["POST"])
def edit_acc_status():
    if check_admin_access():
        user_id = request.form.get("user_id")
        new_status = request.form.get("new_status")
        account_module.changeAccStatus(user_id, new_status)
        return admin_acc_dashboard()
    else:
        return unauthorized()


@app.route("/unauthorized")
def unauthorized():
    flash("Unauthorized to access the link", "error")
    request.path = "/admin"
    return entryPage()
