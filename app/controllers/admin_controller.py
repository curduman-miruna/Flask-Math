from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, unset_jwt_cookies
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from app.utils.decorators.role_required import role_required
from app.services.admin_service import get_admin_metrics
from flask import jsonify
from flask import redirect, url_for
from flask import request

admin_bp = Blueprint("admin", __name__, url_prefix="/web/admin")

# Route: Page view for metrics UI
@admin_bp.route("/metrics")
@role_required(["admin", "superadmin"])
@jwt_required()
def metrics_page():
    try:
        verify_jwt_in_request()
    except Exception:
        unset_jwt_cookies("Token expired")
        return redirect(url_for("web.login"))
    return render_template("admin_metrics.html")

@admin_bp.route("/metrics/raw")
@jwt_required()
@role_required(["admin", "superadmin"])
def secure_metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@admin_bp.route("/metrics/json")
@role_required(["admin", "superadmin"])
@jwt_required()
def metrics_json():
    try:
        metrics = get_admin_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/requests")
@role_required(["superadmin"])
@jwt_required()
def admin_requests():
    try:
        from app.services.admin_request_service import get_all_requests
        requests = get_all_requests()
        return render_template("admin_requests.html", requests=requests)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


