from flask import Blueprint, request, jsonify
from app.services.email_service import send_verification_email
from app.utils.cache import get_cache, set_cache
from flask_jwt_extended import jwt_required
from app.utils.decorators.log_decorator import log_to_postgres
from app.services.user_service import mark_email_verified
import random

email_bp = Blueprint("email", __name__)
VERIFICATION_TTL_SECONDS = 10 * 60  # 15 minutes

@email_bp.route("/send-verification", methods=["POST"])
@log_to_postgres(source="/email/send-verification", service_name="email_service")
@jwt_required()
def send_verification():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Missing email"}), 400

    code = str(random.randint(100000, 999999))

    redis_key = f"verify:{email}"
    set_cache(redis_key, code, VERIFICATION_TTL_SECONDS)

    sent,error = send_verification_email(email, code)
    if sent:
        return jsonify({"message": "Verification code sent"}), 200
    else:
        return jsonify({"error": error}), 500

@email_bp.route("/verify-code", methods=["POST"])
@log_to_postgres(source="/email/verify-code", service_name="email_service")
@jwt_required()
def verify_code():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    if not email or not code:
        return jsonify({"error": "Missing email or code"}), 400

    redis_key = f"verify:{email}"
    stored_code = get_cache(redis_key)

    if stored_code is None:
        return jsonify({"error": "Code expired or not found"}), 400

    if stored_code != code:
        return jsonify({"error": "Invalid code"}), 400

    set_cache(redis_key, "", 1)
    mark_email_verified(email)
    return jsonify({"message": "Code verified"}), 200
