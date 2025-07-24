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
            set_cache(cache_key, result_json["result"], ttl)

            return jsonify({"result": result_json["result"], "cached": False}), status
        return wrapper
    return decorator
