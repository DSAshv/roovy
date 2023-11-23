from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models import *
from app import db
def signup(user_id, email, name, role, password, status='live'):
    try:
        new_user = User(user_id=user_id, email=email, name=name, role=role, status=status)
        credentials = UserCredentials(user_id=user_id, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.add(credentials)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False

def authorizeUser(email, password, role):
    try:
        result = db.session.query(User).join(UserCredentials).filter(
            User.email == email,
            User.role == role
        ).one_or_none()

        if (result is not None and check_password_hash(result.credentials[0].password, password)):
            return (True, result.user_id, result.status)
        else:
            return (False, None, None)



    except Exception as e:
        return (False, None, None)


def updateProfile(request, user_id):
    try:
        user = User.query.get(user_id)
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        credentials.password = generate_password_hash(request.form.get('password'))

        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False


def getUser(uid):
    return User.query.get(uid)
