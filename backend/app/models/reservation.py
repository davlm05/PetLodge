from datetime import datetime, timezone

from app.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"
    __table_args__ = (
        db.Index("ix_reservations_owner_id", "owner_id"),
        db.Index("ix_reservations_pet_id", "pet_id"),
        db.Index("ix_reservations_room_id", "room_id"),
        db.Index("ix_reservations_status", "status"),
        db.Index("ix_reservations_check_in_date", "check_in_date"),
        db.Index("ix_reservations_check_out_date", "check_out_date"),
    )

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    lodging_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    total_price = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
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
    owner = db.relationship("User", back_populates="reservations")
    pet = db.relationship("Pet", back_populates="reservations")
    room = db.relationship("Room", back_populates="reservations")
    services = db.relationship(
        "ReservationService", back_populates="reservation", lazy="select"
    )

    def __repr__(self):
        return f"<Reservation {self.id} pet={self.pet_id} room={self.room_id} {self.status}>"
