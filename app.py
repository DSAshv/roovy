from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)

app.config['SONG_UPLOAD_FOLDER'] = "static/songs"
app.config['THUMBNAIL_UPLOAD_FOLDER'] = "static/thumbnails"
Session(app)
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
