from flask import Blueprint, request, jsonify
from app.services.math_service import power, fibonacci, factorial
from app.utils.decorators.cache_decorator import cache_response

math_bp = Blueprint('math', __name__, url_prefix='/api/math')

@math_bp.route("/pow", methods=["POST"])
@cache_response(lambda req: f"pow:{req.json.get('base')}:{req.json.get('exponent')}")
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
@cache_response(lambda req: f"fib:{req.json.get('n')}")
def fibonacci_endpoint():
    data = request.get_json()
    n = int(data.get("n"))
    result = fibonacci(n)
    return jsonify({"result": result})

@math_bp.route("/factorial", methods=["POST"])
@cache_response(lambda req: f"fact:{req.json.get('n')}")
def factorial_endpoint():
    data = request.get_json()
    try:
        n = int(data.get("n"))
        result = factorial(n)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400