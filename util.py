import uuid
from datetime import datetime

from flask import session

from models import Song


def generate_unique_string():
    unique_string = str(uuid.uuid4())
    return unique_string


def get_uid():
    return session.get("uid")


def getSongToEdit(song_id):
    return Song.query.get(song_id)


def formatDate(created_on_str):
    return datetime.fromisoformat(created_on_str)
