from app.extensions import ma
from marshmallow import fields


class RoomSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    number = fields.String()
    name = fields.String()
    room_type = fields.String()
    capacity = fields.Integer()
    price_per_night = fields.Float()
    description = fields.String()
    is_active = fields.Boolean()


class ServiceSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    price = fields.Float()
    is_active = fields.Boolean()
