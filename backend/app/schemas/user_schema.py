from app.extensions import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(dump_only=True)
    full_name = fields.String(required=True)
    id_number = fields.String(dump_only=True)
    phone = fields.String()
    address = fields.String()
    role = fields.String(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(ma.Schema):
    full_name = fields.String(load_default=None)
    phone = fields.String(load_default=None)
    address = fields.String(load_default=None)
