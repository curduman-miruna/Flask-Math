from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import admin_request_service, user_service
from app.utils.decorators.log_decorator import log_to_postgres
from app.utils.decorators.role_required import role_required

admin_req_bp = Blueprint("admin_request", __name__)

@admin_req_bp.route("/request", methods=["POST"])
@log_to_postgres(source="/admin_request/request", service_name="admin_request_service")
@role_required(["user"])
@jwt_required()
def request_admin():
    user_id = get_jwt_identity()
    try:
        result = admin_request_service.create_admin_request(user_id)
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@admin_req_bp.route("/all", methods=["GET"])
@role_required(["superadmin"])
@jwt_required()
def list_requests():
    result = admin_request_service.get_all_requests()
    return jsonify(result), 200

@admin_req_bp.route("/resolve/<int:request_id>", methods=["POST"])
@log_to_postgres(source="/admin_request/resolve_request", service_name="admin_request_service")
@role_required(["superadmin"])
@jwt_required()
def resolve_admin_request(request_id):
    data = request.get_json()
    approve = data.get("approve")  # boolean
    try:
        result = admin_request_service.resolve_request(request_id, approve)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@admin_req_bp.route("/user_request", methods=["GET"])
@log_to_postgres(source="/admin_request/request", service_name="admin_request_service")
@role_required(["user"])
@jwt_required()
def get_user_request():
    user_id = get_jwt_identity()
    try:
        request_data = admin_request_service.get_user_request(user_id)
        if not request_data:
            return jsonify({"error": "No request found"}), 404
        return jsonify(request_data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
