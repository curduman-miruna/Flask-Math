# app/services/auth_service.py
from app.models.user import User
from app.database import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def generate_tokens(user):
    identity = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"]
    }
    access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(identity=identity)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def register_user(full_name, username, email, phone_number, password):
    existing_user = User.query.filter(
        (User.email == email) | (User.phone_number == phone_number),
        User.is_current == True
    ).first()
    if existing_user:
        raise ValueError("A user with this email or phone number already exists")

    role = "superadmin" if User.query.count() == 0 else "user"
    user = User(full_name, username, email, phone_number, password, role)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Failed to register user due to a constraint violation")

    return user

def login_user(email, password):
    user = User.query.filter_by(email=email, is_current=True).first()
    if not user or not user.check_password(password):
        raise ValueError("Invalid credentials")
    return user