import decimal

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.utils.decorators.log_decorator import log_to_postgres
from app.services.math_service import power, fibonacci, factorial
from app.utils.decorators.cache_decorator import cache_response
from app.schemas.math_schema import PowerInput, FibonacciInput, FactorialInput
from app.utils.log_to_redis import log_to_redis

math_bp = Blueprint("math", __name__, url_prefix="/api/math")

def to_scientific_str(val, precision=5):
    s = str(val)
    exponent = len(s) - 1
    significand = s[:precision].ljust(precision, '0')  # pad if needed
    return f"{significand[0]}.{significand[1:]}e+{exponent}"


@math_bp.route("/pow", methods=["POST"])
@cache_response(lambda req: f"pow:{req.json.get('base')}:{req.json.get('exponent')}")
@log_to_postgres(source="/math/pow", service_name="math_service")
@jwt_required()
def pow_endpoint():
    try:
        data = PowerInput(**request.get_json())
        result = power(data.base, data.exponent)

        log_to_redis(level="INFO", message=f"Power calculation: {data.base}^{data.exponent} = {result}")
        val_string = str(result)
        val_scientific_str = to_scientific_str(result)
        result = { "string": val_string, "scientific": val_scientific_str }
        return jsonify({
            "result": result
        }), 200

    except ValidationError as ve:
        log_to_redis(level="ERROR", message=f"Validation error: {ve.errors()}")
        return jsonify({"validation_error": ve.errors()}), 422

    except Exception as e:
        log_to_redis(level="ERROR", message=f"Error in power calculation: {str(e)}")
        return jsonify({"error": str(e)}), 400


@math_bp.route("/fibonacci", methods=["POST"])
@cache_response(lambda req: f"fib:{req.json.get('n')}")
@log_to_postgres(source="/math/fibonacci", service_name="math_service")
@jwt_required()
def fibonacci_endpoint():
    try:
        data = FibonacciInput(**request.get_json())
        result = fibonacci(data.n)
        log_to_redis(level="INFO", message=f"Fibonacci calculation for n={data.n}: {result}")

        if result > 2**31 - 1:
            log_to_redis(level="WARNING", message=f"Fibonacci result for n={data.n} exceeds int limit")
        val_string = str(result)
        val_scientific_str = to_scientific_str(result)
        result = { "string": val_string, "scientific": val_scientific_str }
        return jsonify({
            "result": result
        }), 200
    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 400
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

        log_to_redis(level="INFO", message=f"Factorial calculation for n={data.n}: {result}")
        val_string = str(result)
        val_scientific_str = to_scientific_str(result)
        result = { "string": val_string, "scientific": val_scientific_str }
        return jsonify({
            "result": result
        }), 200

    except ValidationError as ve:
        log_to_redis(level="ERROR", message=f"Validation error: {ve.errors()}")
        return jsonify({"validation_error": ve.errors()}), 422

    except Exception as e:
        log_to_redis(level="ERROR", message=f"Error in factorial calculation: {str(e)}")
        return jsonify({"error": str(e)}), 400
