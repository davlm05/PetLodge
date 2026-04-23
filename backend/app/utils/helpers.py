from flask import jsonify


def success_response(data=None, message="Operación exitosa", status_code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(error, code="ERROR", status_code=400):
    return jsonify({"success": False, "error": error, "code": code}), status_code
