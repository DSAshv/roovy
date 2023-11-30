import account_module
import creator_module
from landing_pages import userLandingPage, adminLandingPage, creatorLandingPage
from util import generate_unique_string, getSongFromId, getAlbumFromId
from app import app
from flask import render_template, redirect, request, flash, url_for, session

@app.route("/")
def index():
    if not session.get("uid"):
        return redirect("/user"),200
    else:
        if (session.get("role") == "user"):
            return userLandingPage()
        elif (session.get("role") == "admin"):
            return adminLandingPage()
        elif(session.get("role") == "creator"):
            return creatorLandingPage()
        else:
            return ({"error":"undefined role"}),400
    return ({"error":"Internal server error"}),500


@app.route("/user", methods=["GET"])
@app.route("/creator", methods=["GET"])
@app.route("/admin", methods=["GET"])
def entryPage():
    if request.path == "/user":
        if(session.get("uid") and session.get("role") == 'user'):
           return userLandingPage(),200
        return render_template("user_entry.html"),200
    elif request.path == "/creator":
        if (session.get("uid") and session.get("role") == 'creator'):
            return creatorLandingPage(),200
        return render_template("creator_entry.html"),200
    elif request.path == "/admin":
        if (session.get("uid") and session.get("role") == 'admin'):
            return adminLandingPage(),200
        return render_template("admin_login.html"),200


@app.route("/user-sign-in", methods=["POST"])
@app.route("/creator-sign-in", methods=["POST"])
@app.route("/admin-sign-in", methods=["POST"])
def signIn():
    email = request.form.get("email")
    password = request.form.get("password")
    if request.path == "/user-sign-in":
        role = "user"
    elif request.path == "/creator-sign-in":
        role = "creator"
    elif request.path == "/admin-sign-in":
        role = "admin"

    authorization, uid, status = account_module.authorizeUser(email, password, role)
    if (authorization):
        session["uid"] = uid
        session["role"] = role
        return redirect(url_for('index')),200
    else:
        flash("Signin failed. Please try again with correct credentials.", "error")
        return "incorrect credentials"


@app.route("/user-sign-up", methods=["POST"])
@app.route("/creator-sign-up", methods=["POST"])
def signUp():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    if (request.path == "/user-sign-up"):
        role = "user"
    elif (request.path == "/creator-sign-up"):
        role = "creator"
    else:
        return ({"error":"Undefined role"}),400
    uid = generate_unique_string()
    if (account_module.signup(uid, email, name, role, password)):
        session["uid"] = uid
        session["role"] = role
        return redirect(url_for("index")),200
    flash("Signup failed. Please try again with different email.", "error")
    return ({"error":"signup failed"}),500

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/create_album', methods=['GET', 'POST'])
def createAlbum():
    if (request.method == 'GET'):
        return creatorLandingPage("create_album"), 200
    if (creator_module.addAlbumToDB(request)):
        return 'album created', 200
    else:
        flash("Album creation failed. Please try again.", "error")
        return ({"error": "album creation failed"}), 500

@app.route('/create_song', methods=['GET', 'POST'])
def createSong():
    if (request.method == 'GET'):
        return creatorLandingPage("create_song")
    if (creator_module.addSongToDB(request)):
        return 'song created', 200
    else:
        flash("Song creation failed. Please try again.", "error")
        return ({"error": "song creation failed"}), 500


@app.route('/create_playlist', methods=['POST'])
def createPlaylist():
    if (creator_module.addPlaylist(request.form.get("name"))):
        return redirect("../playlists"), 200
    else:
        flash("Playlist creation failed. Please try again.", "error")
        return ({"error": "Playlist creation failed"}), 500

@app.route('/edit_song/<string:song_id>', methods=['GET', 'POST'])
def editSong(song_id):
    if (request.method == 'GET'):
        return creatorLandingPage("edit_song", request)
    if (creator_module.editSongInDB(request, getSongFromId(song_id))):
        return redirect("../mysongs"), 200
    else:
        flash("Song editing failed. Please try again.", "error")
        return ({"error": "song creation failed"}), 500

@app.route('/edit_album/<string:album_id>', methods=['GET', 'POST'])
def editAlbum(album_id):
    album = getAlbumFromId(album_id)
    if request.method == 'POST':
        if creator_module.editAlbumInDB(request, album):
            flash("Album edited successfully", "success")
            return redirect("../myalbums"), 200
        else:
            flash("Error editing the album. Please try again.", "error"), 500

    return creatorLandingPage("edit_album", request), 200


@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    user_id = session.get("uid")
    if (not user_id):
        flash("Authenticate first", "error")
        return redirect(url_for("index"))
    if request.method == 'POST':
        if (account_module.updateProfile(request, user_id)):
            flash("Profile updated successfully", "success")
        else:
            flash("Email is already in use. Please choose another one.", "error")

    return render_template('profile.html', user=account_module.getUser(user_id))

@app.route('/songs', methods=['GET'])
@app.route('/albums', methods=['GET'])
@app.route('/mysongs', methods=['GET'])
@app.route('/myalbums', methods=['GET'])
@app.route('/playlists', methods=['GET'])
def getContent():
    content = request.path.lstrip("/")
    if session.get("role") == "user":
        return userLandingPage(content)
    elif session.get("role") == "creator":
        return creatorLandingPage(content)
    else:
        flash("Cannot load content.", "error")
        return ({"error": "cannot get content."}), 500


@app.route('/album/<string:id>', methods=['GET'])
@app.route('/playlist/<string:id>', methods=['GET'])
def getAlbumDetails(id):
    content = "getModuleContent"
    if session.get("role") == "user":
        return userLandingPage(content, request)
    elif session.get("role") == "creator":
        return creatorLandingPage(content, request)
    else:
        flash("Cannot load content.", "error")
        return ({"error": "cannot get content."}), 500


@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    if (creator_module.addSongToPlaylist(request.form.get("song_id"), request.form.get("playlist_id"))):
        return redirect("../playlist/" + request.form.get("playlist_id")), 200
    else:
        flash("Failed to add to playlist. Please try again.", "error")
        return ({"error": "Failed to add to playlist"}), 500


@app.route('/delete_album/<album_id>', methods=['POST'])
def delete_album(album_id):
    if request.method == 'POST':
        if creator_module.deleteAlbum(album_id):
            return redirect("../myalbums"), 200
        else:
            return {"error": "Album not found or error occurred"}, 404


@app.route('/delete_song/<song_id>', methods=['POST'])
def delete_song(song_id):
    if request.method == 'POST':
        if creator_module.deleteSong(song_id):
            return redirect("../mysongs"), 200
        else:
            return {"error": "Song not found or error occurred"}, 404


@app.route('/delete_playlist/<playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    if request.method == 'POST':
        if creator_module.deletePlaylist(playlist_id):
            return redirect("../playlists"), 200
        else:
            return {"error": "Song not found or error occurred"}, 404


@app.route('/add_rating', methods=['POST'])
def add_rating():
    if request.method == 'POST' and creator_module.addRating(request.form.get("song_id"), request.form.get('rating')):
        return redirect("../")
    else:
        return redirect("../")


@app.route('/play_song/<string:song_id>', methods=['POST'])
def play(song_id):
    if request.method == 'POST':
        return creator_module.playSong(song_id)


if __name__ == '__main__':
    app.run(debug=True)
