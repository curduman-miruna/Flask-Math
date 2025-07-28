from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.utils.decorators.log_decorator import log_to_postgres
from app.services.math_service import power, fibonacci, factorial
from app.utils.decorators.cache_decorator import cache_response
from app.schemas.math_schema import PowerInput, FibonacciInput, FactorialInput

math_bp = Blueprint("math", __name__, url_prefix="/api/math")


@math_bp.route("/pow", methods=["POST"])
@cache_response(lambda req: f"pow:{req.json.get('base')}:{req.json.get('exponent')}")
@log_to_postgres(source="/math/pow", service_name="math_service")
@jwt_required()
def pow_endpoint():
    try:
        data = PowerInput(**request.get_json())
        result = power(data.base, data.exponent)
        return jsonify({"result": str(result)}), 200
    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@math_bp.route("/fibonacci", methods=["POST"])
@cache_response(lambda req: f"fib:{req.json.get('n')}")
@log_to_postgres(source="/math/fibonacci", service_name="math_service")
@jwt_required()
def fibonacci_endpoint():
    try:
        data = FibonacciInput(**request.get_json())
        result = fibonacci(data.n)
        return jsonify({"result": str(result)}), 200
    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@math_bp.route("/factorial", methods=["POST"])
@cache_response(lambda req: f"fact:{req.json.get('n')}")
@log_to_postgres(source="math/factorial/", service_name="math_service")
@jwt_required()
def factorial_endpoint():
    try:
        data = FactorialInput(**request.get_json())
        result = factorial(data.n)
        return jsonify({"result": str(result)}), 200
    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 400
