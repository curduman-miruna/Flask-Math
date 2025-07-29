from app.models.admin_request import AdminRequest
from app.models.user import User
from app.database import db
from app.utils.log_to_redis import log_to_redis


def create_admin_request(user_id):
    existing = AdminRequest.query.filter_by(user_id=user_id, status="PENDING").first()
    if existing:
        log_to_redis(
            level="ERROR", message=f"User {user_id} already has a pending request."
        )
        raise ValueError("You already have a pending request.")

    new_request = AdminRequest(user_id=user_id)
    db.session.add(new_request)
    db.session.commit()
    log_to_redis(level="INFO", message=f"Admin request created for user {user_id}")
    return new_request.to_dict()


def get_all_requests():
    return [
        r.to_dict()
        for r in AdminRequest.query.order_by(AdminRequest.requested_at.desc()).all()
    ]


def get_user_request(user_id):
    request = AdminRequest.query.filter_by(user_id=user_id).first()
    if not request:
        log_to_redis(
            level="ERROR", message=f"No pending request found for user {user_id}."
        )
        return None
    log_to_redis(level="INFO", message=f"Request found for user {user_id}.")
    return request.to_dict()


def resolve_request(request_id, approve: bool):
    request = AdminRequest.query.get(request_id)
    if not request:
        log_to_redis(level="ERROR", message=f"Request {request_id} not found.")
        raise ValueError("Request not found.")

    if request.status != "PENDING":
        log_to_redis(level="ERROR", message=f"Request {request_id} already resolved.")
        raise ValueError("Request already resolved.")

    request.status = "APPROVED" if approve else "REJECTED"
    request.resolved_at = db.func.now()
    db.session.commit()

    if approve:
        user = User.query.filter_by(sk=request.user_id).first()
        if user:
            user.role = "admin"
            db.session.commit()
    log_to_redis(level="INFO", message=f"Request {request_id} resolved.")
    return request.to_dict()
