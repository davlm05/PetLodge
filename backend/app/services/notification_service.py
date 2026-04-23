import threading
from datetime import datetime, timezone

from flask import current_app
from flask_mail import Message

from app.extensions import db, mail
from app.models.notification import Notification
from app.models.notification_template import NotificationTemplate


class NotificationService:

    @staticmethod
    def send_notification(user, event_type, context=None):
        context = context or {}
        template = NotificationTemplate.query.filter_by(
            event_type=event_type, is_active=True
        ).first()

        if not template:
            return

        subject = NotificationService._interpolate(template.subject, context)
        body_html = NotificationService._interpolate(template.body_html, context)

        notification = Notification(
            user_id=user.id,
            template_id=template.id,
            event_type=event_type,
            subject=subject,
            body_html=body_html,
            recipient_email=user.email,
            status="pending",
        )
        db.session.add(notification)
        db.session.commit()

        # Send email asynchronously
        app = current_app._get_current_object()
        thread = threading.Thread(
            target=NotificationService._send_email_async,
            args=(app, notification.id, subject, body_html, user.email),
        )
        thread.start()

    @staticmethod
    def _send_email_async(app, notification_id, subject, body_html, recipient_email):
        with app.app_context():
            notification = Notification.query.get(notification_id)
            try:
                msg = Message(
                    subject=subject,
                    recipients=[recipient_email],
                    html=body_html,
                )
                mail.send(msg)
                notification.status = "sent"
                notification.sent_at = datetime.now(timezone.utc)
            except Exception as e:
                notification.status = "failed"
                notification.error_message = str(e)
            finally:
                db.session.commit()

    @staticmethod
    def _interpolate(text, context):
        for key, value in context.items():
            text = text.replace("{{" + key + "}}", str(value))
        return text

    @staticmethod
    def get_user_notifications(user_id):
        return Notification.query.filter_by(user_id=user_id).order_by(
            Notification.created_at.desc()
        ).all()

    @staticmethod
    def list_templates():
        return NotificationTemplate.query.order_by(
            NotificationTemplate.created_at.desc()
        ).all()

    @staticmethod
    def create_template(data):
        if NotificationTemplate.query.filter_by(event_type=data["event_type"]).first():
            return None, "Ya existe una plantilla para este evento.", "TEMPLATE_EXISTS"

        template = NotificationTemplate(
            event_type=data["event_type"],
            subject=data["subject"],
            body_html=data["body_html"],
            variables=data.get("variables"),
        )
        db.session.add(template)
        db.session.commit()
        return template, None, None

    @staticmethod
    def update_template(template_id, data):
        template = db.session.get(NotificationTemplate, template_id)
        if not template:
            return None, "Plantilla no encontrada.", "TEMPLATE_NOT_FOUND"

        for key, value in data.items():
            if value is not None:
                setattr(template, key, value)

        db.session.commit()
        return template, None, None
