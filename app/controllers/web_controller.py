# app/controllers/web_controller.py
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from app.utils.log_to_redis import log_to_redis
from app.utils.decorators.log_decorator import log_to_postgres

web_bp = Blueprint("web", __name__)


@web_bp.route("/login", methods=["GET"])
@log_to_postgres(source="/web/login", service_name="N/A")
def register():
    log_to_redis(level="INFO", message="Accessed login page")
    return render_template("register.html")


@web_bp.route("/dashboard", methods=["GET"])
@log_to_postgres(source="/web/dashboard", service_name="N/A")
@jwt_required(optional=True)
def dashboard():
    log_to_redis(level="INFO", message="Accessed dashboard page")
    return render_template("dashboard.html")


@web_bp.route("/", methods=["GET"])
@log_to_postgres(source="/web/home", service_name="N/A")
def home():
    log_to_redis(level="INFO", message="Accessed home page")
    return render_template("home.html")


@web_bp.route("/profile", methods=["GET"])
@log_to_postgres(source="/web/profile", service_name="N/A")
@jwt_required()
def profile():
    log_to_redis(level="INFO", message="Accessed profile page")
    return render_template("profile.html")
