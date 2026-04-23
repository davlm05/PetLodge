from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify(success=False, error="Acceso denegado. Se requiere rol de administrador.", code="FORBIDDEN"), 403
        return fn(*args, **kwargs)
    return wrapper


def owner_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "owner":
            return jsonify(success=False, error="Acceso denegado. Se requiere rol de dueño.", code="FORBIDDEN"), 403
        return fn(*args, **kwargs)
    return wrapper
