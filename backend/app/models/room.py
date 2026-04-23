from datetime import datetime, timezone

from app.extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, default=1)
    price_per_night = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    reservations = db.relationship("Reservation", back_populates="room", lazy="dynamic")

    def __repr__(self):
        return f"<Room {self.id} {self.number} ({self.room_type})>"
