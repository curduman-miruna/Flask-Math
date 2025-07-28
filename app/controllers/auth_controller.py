from datetime import timedelta
from flask import Blueprint, request, jsonify
from app.services import auth_service
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from pydantic import ValidationError

from app.utils.decorators.log_decorator import log_to_postgres

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@log_to_postgres(source="/auth/register" ,service_name="auth_service")
async def register():
    try:
        data = RegisterSchema(**request.get_json())
        user = auth_service.register_user(
            full_name=data.full_name,
            username=data.username,
            email=data.email,
            phone_number=data.phone_number,
            password=data.password
        )
        return jsonify(user.to_dict()), 201
    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
@log_to_postgres(source="/auth/login", service_name="auth_service")
def login():
    try:
        data = LoginSchema(**request.get_json())
        user = auth_service.login_user(data.email, data.password)

        access_token = create_access_token(
            identity=str(user.sk),
            additional_claims={
                "role": str(user.role),
                "email": str(user.email)
            },
            expires_delta=timedelta(minutes=30)
        )

        refresh_token = create_refresh_token(identity=str(user.id))

        resp = jsonify({
            "msg": "Login successful",
            "user": user.to_dict()
        })

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200

    except ValidationError as ve:
        return jsonify({"validation_error": ve.errors()}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401

    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@log_to_postgres(source="/auth/refresh", service_name="auth_service")
def refresh_tokens():
    identity = get_jwt_identity()
    new_access = create_access_token(identity=identity)

    resp = jsonify({"msg": "Token refreshed"})
    set_access_cookies(resp, new_access)

    return resp, 200


@auth_bp.route("/logout", methods=["POST"])
@log_to_postgres(source="/auth/logout", service_name="auth_service")
def logout():
    resp = jsonify(msg="Logged out")
    unset_jwt_cookies(resp)
    return resp, 200

