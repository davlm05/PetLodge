from app.extensions import ma
from marshmallow import fields


class SuccessResponseSchema(ma.Schema):
    success = fields.Boolean(dump_default=True)
    data = fields.Raw(allow_none=True)
    message = fields.String()


class ErrorResponseSchema(ma.Schema):
    success = fields.Boolean(dump_default=False)
    error = fields.String(required=True)
    code = fields.String()
