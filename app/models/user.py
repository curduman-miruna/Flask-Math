# app/models/user_model.py
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint, event, and_, UniqueConstraint
from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    sk = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Surrogate Key
    id = db.Column(db.String(36), nullable=False)  # Business Key (UUID)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_current = db.Column(db.Boolean, default=True, nullable=False)
    effective_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    effective_to = db.Column(db.DateTime, nullable=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    phone_verified = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin', 'superadmin')", name='check_valid_role'),
        UniqueConstraint('email', 'is_current', name='uq_current_email'),
        UniqueConstraint('phone_number', 'is_current', name='uq_current_phone')
    )

    def __init__(self, full_name, username, email, phone_number, password, role="user"):
        self.id = str(uuid.uuid4())
        self.full_name = full_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.is_current = True
        self.email_verified = False
        self.phone_verified = False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "sk": self.sk,
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "is_current": self.is_current,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "email_verified": self.email_verified,
            "phone_verified": self.phone_verified
        }

@event.listens_for(User, 'before_update')
def create_user_version(target):
    current_user = db.session.query(User).filter(
        and_(User.id == target.id, User.is_current == True)
    ).first()

    if current_user:
        current_user.is_current = False
        current_user.effective_to = datetime.now()
        db.session.flush()

        new_version = User(
            full_name=target.full_name,
            username=target.username,
            email=target.email,
            phone_number=target.phone_number,
            password="temp",
            role=target.role
        )
        new_version.id = target.id
        new_version.password_hash = target.password_hash
        new_version.email_verified = target.email_verified
        new_version.phone_verified = target.phone_verified
        db.session.add(new_version)

        db.session.expunge(target)
        raise Exception("Direct update not allowed. Use versioning.")
