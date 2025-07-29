from datetime import datetime
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


def update_user_profile(email, **kwargs):
    current_user = get_current_user_by_email(email)
    if not current_user:
        return None

    try:
        current_user.is_current = False
        current_user.effective_to = datetime.now()

        new_user = User(
            full_name=kwargs.get("full_name", current_user.full_name),
            username=kwargs.get("username", current_user.username),
            email=kwargs.get("email", current_user.email),
            phone_number=kwargs.get("phone_number", current_user.phone_number),
            password=current_user.password_hash,
            role=kwargs.get("role", current_user.role),
        )
        new_user.id = current_user.id
        new_user.password_hash = current_user.password_hash
        new_user.email_verified = current_user.email_verified
        new_user.phone_verified = current_user.phone_verified
        new_user.effective_from = datetime.now()
        new_user.is_current = True

        db.session.add(new_user)
        db.session.commit()
        return new_user

    except SQLAlchemyError:
        db.session.rollback()
        return None
