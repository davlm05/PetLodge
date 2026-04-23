from datetime import datetime, timezone

from app.extensions import db


class ReservationService(db.Model):
    __tablename__ = "reservation_services"
    __table_args__ = (
        db.UniqueConstraint(
            "reservation_id", "service_id", name="uq_reservation_service"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservations.id"), nullable=False
    )
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    reservation = db.relationship("Reservation", back_populates="services")
    service = db.relationship("Service")

    @property
    def service_name(self):
        return self.service.name if self.service else None

    def __repr__(self):
        return f"<ReservationService {self.id} res={self.reservation_id} svc={self.service_id}>"
