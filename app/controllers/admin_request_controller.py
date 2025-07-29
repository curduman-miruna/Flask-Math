from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import admin_request_service
from app.utils.decorators.log_decorator import log_to_postgres
from app.utils.decorators.role_required import role_required
from app.utils.log_to_redis import log_to_redis

admin_req_bp = Blueprint("admin_request", __name__)


@admin_req_bp.route("/request", methods=["POST"])
@log_to_postgres(source="/admin_request/request", service_name="admin_request_service")
@role_required(["user"])
@jwt_required()
async def request_admin():
    user_id = get_jwt_identity()
    try:
        result = admin_request_service.create_admin_request(user_id)
        log_to_redis(level="INFO", message=f"User {user_id} created an admin request")
        return jsonify(result), 201
    except ValueError as ve:
        log_to_redis(level="ERROR", message=f"Error creating admin request: {str(ve)}")
        return jsonify({"error": str(ve)}), 400


@admin_req_bp.route("/all", methods=["GET"])
@role_required(["superadmin"])
@jwt_required()
async def list_requests():
    result = admin_request_service.get_all_requests()
    if not result:
        log_to_redis(level="WARNING", message="No requests found")
        return jsonify({"message": "No requests found"}), 404
    log_to_redis(level="INFO", message=f"List all requests: {result}")
    return jsonify(result), 200


@admin_req_bp.route("/resolve/<int:request_id>", methods=["POST"])
@log_to_postgres(
    source="/admin_request/resolve_request", service_name="admin_request_service"
)
@role_required(["superadmin"])
@jwt_required()
async def resolve_admin_request(request_id):
    data = request.get_json()
    approve = data.get("approve")  # boolean
    try:
        result = admin_request_service.resolve_request(request_id, approve)
        if not result:
            log_to_redis(level="WARNING", message=f"Request {request_id}"
                                                  f" not found or already resolved")
            return jsonify({"error": "Request not found or already resolved"}), 404
        log_to_redis(level="INFO", message=f"Request {request_id} "
                                           f"resolved with approval: {approve}")
        return jsonify(result), 200
    except ValueError as e:
        log_to_redis(level="ERROR", message=f"Error resolving request {request_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400


@admin_req_bp.route("/user_request", methods=["GET"])
@log_to_postgres(source="/admin_request/request", service_name="admin_request_service")
@role_required(["user"])
@jwt_required()
async def get_user_request():
    user_id = get_jwt_identity()
    try:
        request_data = admin_request_service.get_user_request(user_id)
        if not request_data:
            log_to_redis(level="WARNING", message=f"No request found for user {user_id}")
            return jsonify({"exists": False}), 200
        log_to_redis(level="INFO", message=f"Fetched request for user {user_id}")
        return jsonify({"exists": True, "request": request_data}), 200
    except ValueError as e:
        log_to_redis(level="ERROR", message=f"Error fetching request for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
