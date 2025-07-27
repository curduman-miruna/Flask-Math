from functools import wraps
from flask import request, jsonify, has_request_context
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.database import db
from app.models.log_event import LogEvent
from uuid import UUID
import time
import traceback

def log_to_postgres(source="API", service_name="N/A", operation=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            user_id = None
            status_code = 200
            response_data = None
            event_type = "API_CALL_SUCCESS"

            try:
                # Execută funcția originală
                response = fn(*args, **kwargs)

                if isinstance(response, tuple):
                    data, status_code = response
                else:
                    data, status_code = response, 200

                try:
                    response_data = data.get_json(silent=True)
                except Exception:
                    response_data = None

                # Dacă status_code >= 400, tratăm ca eroare logică
                if status_code >= 400:
                    event_type = "API_CALL_ERROR"

            except Exception as e:
                # Eroare de execuție
                status_code = 500
                event_type = "API_CALL_ERROR"
                response_data = {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                response = jsonify({"error": str(e)}), 500

            duration_ms = int((time.perf_counter() - start_time) * 1000)

            if has_request_context():
                try:
                    verify_jwt_in_request(optional=True)
                    identity = get_jwt_identity()
                    user_id = UUID(identity) if identity else None
                except Exception:
                    user_id = None

                try:
                    log = LogEvent(
                        source=source,
                        event_type=event_type,
                        operation=operation or fn.__name__,
                        service_name=service_name,
                        status_code=status_code,
                        response_time_ms=duration_ms,
                        user_id=user_id,
                        client_ip=request.remote_addr,
                        request_data=request.get_json(silent=True),
                        response_data=response_data
                    )
                    db.session.add(log)
                    db.session.commit()
                except Exception as log_err:
                    db.session.rollback()
                    print(f"[LOGGING ERROR] {log_err}")

            return response
        return wrapper
    return decorator
