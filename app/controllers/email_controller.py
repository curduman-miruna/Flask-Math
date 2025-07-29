from flask import Blueprint, request, jsonify
from app.services.email_service import send_verification_email
from app.utils.cache import get_cache, set_cache
from flask_jwt_extended import jwt_required
from app.utils.decorators.log_decorator import log_to_postgres
from app.services.user_service import mark_email_verified
import random
from app.utils.log_to_redis import log_to_redis

email_bp = Blueprint("email", __name__)
VERIFICATION_TTL_SECONDS = 10 * 60  # 15 minutes


@email_bp.route("/send-verification", methods=["POST"])
@log_to_postgres(source="/email/send-verification", service_name="email_service")
@jwt_required()
async def send_verification():
    data = request.get_json()
    email = data.get("email")

    if not email:
        log_to_redis(level="ERROR", message="Missing email in request")
        return jsonify({"error": "Missing email"}), 400

    code = str(random.randint(100000, 999999))

    redis_key = f"verify:{email}"
    set_cache(redis_key, code, VERIFICATION_TTL_SECONDS)

    sent, error = send_verification_email(email, code)
    if sent:
        log_to_redis(level="INFO", message=f"Verification email sent to {email}")
        return jsonify({"message": "Verification code sent"}), 200
    else:
        log_to_redis(level="ERROR", message=f"Failed to send verification email: {error}")
        return jsonify({"error": error}), 500


@email_bp.route("/verify-code", methods=["POST"])
@log_to_postgres(source="/email/verify-code", service_name="email_service")
@jwt_required()
async def verify_code():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    if not email or not code:
        log_to_redis(level="ERROR", message="Missing email or code in verification request")
        return jsonify({"error": "Missing email or code"}), 400

    redis_key = f"verify:{email}"
    stored_code = get_cache(redis_key)

    if stored_code is None:
        log_to_redis(level="WARNING", message=f"Verification code for {email} not found or expired")
        return jsonify({"error": "Code expired or not found"}), 400

    if stored_code != code:
        log_to_redis(level="ERROR", message=f"Invalid verification code for {email}")
        return jsonify({"error": "Invalid code"}), 400

    set_cache(redis_key, "", 1)
    mark_email_verified(email)
    log_to_redis(level="INFO", message=f"Email {email} verified successfully")
    return jsonify({"message": "Code verified"}), 200
