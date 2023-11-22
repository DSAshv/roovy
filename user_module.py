from models import *
from app import db
def signup(user_id, email, name, role, password, status='live'):
    try:
        new_user = User(user_id=user_id, email=email, name=name, role=role, status=status)
        credentials = UserCredentials(user_id=user_id, password=password)
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
            UserCredentials.password == password,
            User.role == role
        ).one_or_none()

        if (result is None):
            return (False, None, None)

        return (result is not None, result.user_id, result.status)

    except Exception as e:
        return (False, None, None)
