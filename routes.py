from app import app
from flask import render_template, redirect, request, session
from flask_session import Session

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("uid"):
        return redirect("/user")
    return  # function to create landing page


@app.route("/user", methods=["GET"])
@app.route("/creator", methods=["GET"])
@app.route("/admin", methods=["GET"])
def entryPage():
    if request.path == "/user":
        return render_template("user_entry.html")
    elif request.path == "/creator":
        return render_template("creator_entry.html")
    elif request.path == "/admin":
        return render_template("admin_entry.html")


@app.route("/user-sign-in", methods=["POST"])
@app.route("/creator-sign-in", methods=["POST"])
@app.route("/admin-sign-in", methods=["POST"])
def signIn():
    email = request.form.get("email")
    password = request.form.get("password")
    if request.form.action == "/user-sign-in":
        role = "user"
    elif request.form.action == "/creator-sign-in":
        role = "creator"
    elif request.form.action == "/admin-sign-in":
        role = "admin"

    # authorizeUser()
    session["uid"] = "uid"
    session["role"] = "role"
    return redirect("/")


@app.route("/user-sign-up", methods=["POST"])
@app.route("/creator-sign-up", methods=["POST"])
def signUp():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    # authorizeUser()
    session["uid"] = "uid"
    session["role"] = "role"
    return redirect("/")


@app.route("/logout")
def logout():
    session["uid"] = None
    return redirect("/")
