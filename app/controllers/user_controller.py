from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.services import user_service
from app.utils.decorators.log_decorator import log_to_postgres
from app.utils.log_to_redis import log_to_redis

user_bp = Blueprint("user", __name__)


@user_bp.route("/me", methods=["GET"])
@log_to_postgres(source="/user/me", service_name="user_service")
@jwt_required()
async def get_profile():
    claims = get_jwt()
    email = claims.get("email")
    data = user_service.get_public_profile(email)
    if not data:
        log_to_redis(level="ERROR", message=f"User with email {email} not found")
        return jsonify({"error": "User not found"}), 404
    log_to_redis(level="INFO", message=f"User profile retrieved for {email}")
    return jsonify(data), 200


@user_bp.route("/me/role", methods=["GET"])
@log_to_postgres(source="/user/me/role", service_name="user_service")
@jwt_required()
async def get_user_role():
    claims = get_jwt()
    role = claims.get("role")
    if not role:
        log_to_redis(level="ERROR", message="Role not found in JWT claims")
        return jsonify({"error": "Role not found"}), 404
    log_to_redis(level="INFO", message=f"User role retrieved for {role}")
    return jsonify({"role": role}), 200