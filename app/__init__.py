from flask import Flask
from app.database import init_db
from app.controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)
    init_db(app)
    from app.models import user, admin_request
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    from app.controllers.web_controller import web_bp
    app.register_blueprint(web_bp, url_prefix="/web")
    from app.controllers.math_controller import math_bp
    app.register_blueprint(math_bp, url_prefix="/api/math")
    return app
