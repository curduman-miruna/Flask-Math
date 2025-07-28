from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import user_service
from app.utils.decorators.log_decorator import log_to_postgres

user_bp = Blueprint("user", __name__)

@user_bp.route("/me", methods=["GET"])
@log_to_postgres(source="/user/me", service_name="user_service")
@jwt_required()
async def get_profile():
    user_id = get_jwt_identity()
    claims = get_jwt()
    email = claims.get("email")
    role = claims.get("role")
    data = user_service.get_public_profile(email)
    if not data:
        return jsonify({"error": "User not found"}), 404
    return jsonify(data), 200

@user_bp.route("/me/role", methods=["GET"])
@log_to_postgres(source="/user/me/role", service_name="user_service")
@jwt_required()
async def get_user_role():
    claims = get_jwt()
    role = claims.get("role")
    if not role:
        return jsonify({"error": "Role not found"}), 404

    return jsonify({"role": role}), 200
