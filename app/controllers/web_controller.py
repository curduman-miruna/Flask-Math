# app/controllers/web_controller.py
from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def home():
    return render_template("index.html")

@web_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@web_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@web_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


