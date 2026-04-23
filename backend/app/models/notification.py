from datetime import datetime, timezone

from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"
    __table_args__ = (
        db.Index("ix_notifications_user_id", "user_id"),
        db.Index("ix_notifications_event_type", "event_type"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey("notification_templates.id"), nullable=True
    )
    event_type = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    body_html = db.Column(db.Text, nullable=True)
    recipient_email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = db.relationship("User", back_populates="notifications")
    template = db.relationship("NotificationTemplate")

    def __repr__(self):
        return f"<Notification {self.id} {self.event_type} {self.status}>"
