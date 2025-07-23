from flask import Blueprint, request, jsonify
from app.services.math_service import  power, fibonacci, factorial

math_bp = Blueprint('math', __name__, url_prefix='/api/math')

@math_bp.route("/pow", methods=["POST"])
def pow_endpoint():
    data = request.get_json()
    try:
        base = float(data.get("base"))
        exponent = float(data.get("exponent"))
        result = power(base, exponent)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@math_bp.route("/fibonacci", methods=["POST"])
def fibonacci_endpoint():
    data = request.get_json()
    try:
        n = int(data.get("n"))
        result = fibonacci(n)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@math_bp.route("/factorial", methods=["POST"])
def factorial_endpoint():
    data = request.get_json()
    try:
        n = int(data.get("n"))
        result = factorial(n)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
