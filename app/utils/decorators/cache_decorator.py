from functools import wraps
from flask import request, jsonify
from app.utils.cache import get_cache, set_cache


def cache_response(cache_key_func, ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = cache_key_func(request)

            cached = get_cache(cache_key)
            if cached is not None:
                return jsonify({"result": cached, "cached": True})

            response = func(*args, **kwargs)
            if isinstance(response, tuple):
                data, status = response
            else:
                data, status = response, 200

            result_json = data.get_json()
            print(result_json)

            if not result_json:
                return jsonify({"error": "Empty or invalid JSON response"}), 500
            if "validation_error" in result_json:
                return (
                    jsonify(
                        {
                            "error": "Validation error",
                            "msg": [
                                err.get("msg")
                                for err in result_json["validation_error"]
                            ],
                        }
                    ),
                    400,
                )
            if "result" not in result_json:
                return (
                    jsonify(
                        {"error": f"Missing 'result' key in response {result_json}"}
                    ),
                    500,
                )
            if "string" not in result_json["result"]:
                return (
                    jsonify(
                        {"error": f"Missing 'string' key in 'result' {result_json}"}
                    ),
                    500,
                )
            if "scientific" not in result_json["result"]:
                return (
                    jsonify(
                        {"error": f"Missing 'scientific' key in 'result' {result_json}"}
                    ),
                    500,
                )

            set_cache(
                cache_key,
                {
                    "string": result_json["result"]["string"],
                    "scientific": result_json["result"]["scientific"],
                },
                ttl,
            )

            return (
                jsonify(
                    {
                        "result": {
                            "string": result_json["result"]["string"],
                            "scientific": result_json["result"]["scientific"],
                        },
                        "cached": False,
                    }
                ),
                status,
            )

        return wrapper

    return decorator
