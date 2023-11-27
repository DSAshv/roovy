import account_module
import creator_module
from landing_pages import userLandingPage, adminLandingPage, creatorLandingPage
from models import Album
from util import generate_unique_string
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


@app.route('/edit_song/<string:song_id>', methods=['GET', 'POST'])
def editSong():
    if (request.method == 'GET'):
        return creatorLandingPage("edit_song", request)
    if (creator_module.editSongInDB(request.form)):
        return 'song edited', 200
    else:
        flash("Song editing failed. Please try again.", "error")
        return ({"error": "song creation failed"}), 500


@app.route('/edit_album/<string:album_id>', methods=['GET', 'POST'])
def edit_album():
    album = creator_module.getSongToEdit(request.path.album_id)
    if request.method == 'POST':
        if creator_module.editAlbum(request, album):
            flash("Album edited successfully", "success")
            return redirect(url_for('index')), 200
        else:
            flash("Error editing the album. Please try again.", "error"), 500

    return render_template('edit_album.html', album=album), 200


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
