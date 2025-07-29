from flask import Flask, redirect
from app.database import init_db
from app.controllers.auth_controller import auth_bp
import os
from flask_jwt_extended import JWTManager, get_jwt
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from app.controllers.web_controller import web_bp
from app.controllers.math_controller import math_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.user_controller import user_bp
from app.controllers.email_controller import email_bp
from app.controllers.admin_request_controller import admin_req_bp
from prometheus_flask_exporter import PrometheusMetrics
from app.email_extension import mail
import sys
sys.set_int_max_str_digits(0)

def create_app():
    app = Flask(__name__)

    init_db(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = os.getenv("JWT_TOKEN_LOCATION").split(",")
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SECURE"] = os.getenv("JWT_COOKIE_SECURE")
    app.config["JWT_COOKIE_SAMESITE"] = os.getenv("JWT_COOKIE_SAMESITE")
    app.config["JWT_ACCESS_COOKIE_PATH"] = os.getenv("JWT_ACCESS_COOKIE_PATH")
    app.config["JWT_REFRESH_COOKIE_PATH"] = os.getenv("JWT_REFRESH_COOKIE_PATH")

    @app.route("/")
    def index():
        return redirect("/web")

    JWTManager(app)

    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            return {"user": {"email": claims.get("email"), "role": claims.get("role")}}
        except Exception:
            return {"user": None}

    PrometheusMetrics(app, path=None)

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(web_bp, url_prefix="/web")
    app.register_blueprint(math_bp, url_prefix="/api/math")
    app.register_blueprint(admin_bp, url_prefix="/web/admin")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(email_bp, url_prefix="/api/email")
    app.register_blueprint(admin_req_bp, url_prefix="/api/admin_request")
    return app
