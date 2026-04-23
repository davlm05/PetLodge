from app.extensions import ma
from marshmallow import fields


class NotificationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    event_type = fields.String()
    subject = fields.String()
    recipient_email = fields.Email()
    status = fields.String()
    error_message = fields.String()
    sent_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)


class NotificationTemplateSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    event_type = fields.String()
    subject = fields.String()
    body_html = fields.String()
    variables = fields.Raw()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class NotificationTemplateCreateSchema(ma.Schema):
    event_type = fields.String(required=True)
    subject = fields.String(required=True)
    body_html = fields.String(required=True)
    variables = fields.Raw(load_default=None)


class NotificationTemplateUpdateSchema(ma.Schema):
    subject = fields.String(load_default=None)
    body_html = fields.String(load_default=None)
    variables = fields.Raw(load_default=None)
    is_active = fields.Boolean(load_default=None)
