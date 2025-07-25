from flask import Flask
from app.database import init_db
from app.controllers.auth_controller import auth_bp
import os
from flask_jwt_extended import JWTManager
from app.models import user, admin_request, log_event
from app.controllers.web_controller import web_bp
from app.controllers.math_controller import math_bp

def create_app():
    app = Flask(__name__)
    init_db(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # sau True, dar trebuie să trimiți X-CSRF-TOKEN
    app.config["JWT_COOKIE_SECURE"] = False        # True doar dacă ești pe HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"      # pentru app clasic Flask
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/api/auth/refresh"
    jwt = JWTManager(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(web_bp, url_prefix="/web")
    app.register_blueprint(math_bp, url_prefix="/api/math")
    return app
