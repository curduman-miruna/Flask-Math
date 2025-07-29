from app.models.user import User
from app.database import db
from sqlalchemy.exc import SQLAlchemyError


def get_current_user_by_email(email):
    try:
        return User.query.filter_by(email=email, is_current=True).first()
    except SQLAlchemyError:
        return None


def get_current_user_by_id(user_id):
    try:
        return User.query.filter_by(id=user_id, is_current=True).first()
    except SQLAlchemyError:
        return None


def get_public_profile(email):
    user = get_current_user_by_email(email)
    if not user:
        return None
    return user.to_public_dict()


def mark_email_verified(email):
    user = get_current_user_by_email(email)
    if not user:
        return None

    user.email_verified = True
    db.session.commit()
    return user


def mark_phone_verified(user_id):
    user = get_current_user_by_email(user_id)
    if not user:
        return None

    user.phone_verified = True
    db.session.commit()
    return user
