# app/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from app.services import auth_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        user = auth_service.register_user(
            full_name=data["full_name"],
            username=data["username"],
            email=data["email"],
            phone_number=data["phone_number"],
            password=data["password"]
        )
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        user = auth_service.login_user(
            email=data["email"],
            password=data["password"]
        )
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401