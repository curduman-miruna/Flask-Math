# app/controllers/web_controller.py
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

web_bp = Blueprint("web", __name__)

@web_bp.route("/login", methods=["GET"])
def register():
    return render_template("register.html")

@web_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    return render_template("dashboard.html")

@web_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")


