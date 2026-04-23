from app.extensions import ma
from marshmallow import fields, validate


class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    full_name = fields.String(required=True)
    id_number = fields.String(required=True)
    phone = fields.String(load_default=None)
    address = fields.String(load_default=None)


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class ChangePasswordSchema(ma.Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8))
