from app.database import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import MetaData

class LogEvent(db.Model):
    __tablename__ = "event_logs"
    __table_args__ = {"schema": "logs"}

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    source = db.Column(db.String(255))
    event_type = db.Column(db.String(100))
    operation = db.Column(db.String(100), nullable=True)
    service_name = db.Column(db.String(100), nullable=True)
    status_code = db.Column(db.Integer, nullable=True)
    response_time_ms = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.sk'), nullable=False)
    client_ip = db.Column(db.String(50), nullable=True)
    request_data = db.Column(JSONB)
    response_data = db.Column(JSONB)
