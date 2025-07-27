# app/controllers/web_controller.py
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

from app.utils.decorators.log_decorator import log_to_postgres

web_bp = Blueprint("web", __name__)

@web_bp.route("/login", methods=["GET"])
@log_to_postgres(source="/web/login", service_name="N/A")
def register():
    return render_template("register.html")

@web_bp.route("/dashboard", methods=["GET"])
@log_to_postgres(source="/web/dashboard", service_name="N/A")
@jwt_required(optional=True)
def dashboard():
    from flask_jwt_extended import verify_jwt_in_request, get_jwt
    from flask import redirect, url_for
    try:
        verify_jwt_in_request()
    except Exception:
        return redirect(url_for("web.home"))
    return render_template("dashboard.html")

@web_bp.route("/", methods=["GET"])
@log_to_postgres(source="/web/home", service_name="N/A")
def home():
    return render_template("home.html")

@web_bp.route("/profile", methods=["GET"])
@log_to_postgres(source="/web/profile", service_name="N/A")
@jwt_required(optional=True)
def profile():
    from flask_jwt_extended import verify_jwt_in_request, get_jwt
    from flask import redirect, url_for
    try:
        verify_jwt_in_request()
    except Exception:
        return redirect(url_for("web.home"))
    return render_template("profile.html")




