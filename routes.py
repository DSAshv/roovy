import user_module
from flask import render_template, redirect, request, session, Flask, Blueprint, url_for

from landing_pages import userLandingPage, adminLandingPage, creatorLandingPage
from util import generate_unique_string
from app import app
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

    authorization, uid, status = user_module.authorizeUser(email, password, role)
    if (authorization):
        session["uid"] = uid
        session["role"] = role
        return redirect(url_for('index')),200
    else:
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
    if (user_module.signup(uid, email, name, role, password)):
        session["uid"] = uid
        session["role"] = role
        return redirect(url_for("index")),200

    return ({"error":"signup failed"}),500


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
