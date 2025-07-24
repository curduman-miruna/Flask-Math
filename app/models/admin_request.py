# app/models/admin_request.py
from app.database import db
from datetime import datetime

class AdminRequest(db.Model):
    __tablename__ = 'admin_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.sk'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    resolved_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", backref="admin_requests")

    def __init__(self, user_id):
        self.user_id = user_id
        self.status = "pending"
        self.requested_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "requested_at": self.requested_at,
            "resolved_at": self.resolved_at
        }