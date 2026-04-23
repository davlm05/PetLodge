from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.reservation_schema import (
    ReservationSchema, 
    ReservationCreateSchema, 
    ReservationUpdateSchema, 
    ReservationStatusUpdateSchema
)
from app.services.reservation_service import ReservationService
from app.services.notification_service import NotificationService
from app.models.user import User
from app.utils.helpers import success_response, error_response
from app.utils.decorators import admin_required

blp = Blueprint(
    "reservations", __name__,
    url_prefix="/api/v1/reservations",
    description="Gestión de reservas",
)


@blp.route("/")
class ReservationList(MethodView):
    @jwt_required()
    @blp.arguments(ReservationCreateSchema)
    @blp.doc(summary="Crear reserva", description="Crea una nueva reserva para una mascota del dueño autenticado")
    def post(self, data):
        owner_id = int(get_jwt_identity())
        reservation, err, code = ReservationService.create_reservation(owner_id, data)
        if err:
            status_map = {
                "INVALID_CHECK_IN": 400,
                "PET_NOT_FOUND": 404,
                "ROOM_NOT_FOUND": 404,
                "RESERVATION_CONFLICT": 409,
                "SERVICES_NOT_ALLOWED": 400,
                "SERVICE_NOT_FOUND": 404,
                "DUPLICATE_SERVICES": 400,
            }
            return error_response(err, code, status_map.get(code, 400))

        # Send confirmation notification
        user = User.query.get(owner_id)
        NotificationService.send_notification(
            user,
            "reservation_confirmed",
            {
                "user_name": user.full_name,
                "pet_name": reservation.pet.name,
                "check_in_date": str(reservation.check_in_date),
                "check_out_date": str(reservation.check_out_date),
                "room_number": reservation.room.number,
            },
        )

        return success_response(
            ReservationSchema().dump(reservation),
            "Reserva creada exitosamente.",
            201,
        )

    @jwt_required()
    @blp.doc(summary="Ver historial de reservas", description="Lista todas las reservas del dueño autenticado")
    def get(self):
        owner_id = int(get_jwt_identity())
        reservations = ReservationService.list_reservations(owner_id)
        return success_response(ReservationSchema(many=True).dump(reservations))


@blp.route("/<int:reservation_id>")
class ReservationDetail(MethodView):
    @jwt_required()
    @blp.doc(summary="Detalle de reserva", description="Obtiene los datos de una reserva específica")
    def get(self, reservation_id):
        owner_id = int(get_jwt_identity())
        reservation, err, code = ReservationService.get_reservation(reservation_id, owner_id)
        if err:
            return error_response(err, code, 404)
        return success_response(ReservationSchema().dump(reservation))

    @jwt_required()
    @blp.doc(summary="Cancelar reserva", description="Cancela una reserva existente")
    def delete(self, reservation_id):
        owner_id = int(get_jwt_identity())
        reservation, err, code = ReservationService.cancel_reservation(reservation_id, owner_id)
        if err:
            status = 404 if code == "RESERVATION_NOT_FOUND" else 400
            return error_response(err, code, status)
        # Send cancellation notification
        user = User.query.get(owner_id)
        NotificationService.send_notification(
            user,
            "reservation_cancelled",
            {
                "user_name": user.full_name,
                "pet_name": reservation.pet.name,
                "check_in_date": str(reservation.check_in_date),
                "check_out_date": str(reservation.check_out_date),
                "room_number": reservation.room.number,
            },
        )

        return success_response(
            ReservationSchema().dump(reservation),
            "Reserva cancelada exitosamente.",
        )

    @jwt_required()
    @blp.arguments(ReservationUpdateSchema)
    @blp.doc(summary="Modificar reserva", description="Modifica las fechas, habitación y/o servicios de una reserva")
    def put(self, data, reservation_id):
        owner_id = int(get_jwt_identity())
        reservation, err, code = ReservationService.update_reservation(reservation_id, owner_id, data)
        if err:
            status_map = {
                 "RESERVATION_NOT_FOUND": 404,
                 "CANNOT_MODIFY": 400,
                 "INVALID_CHECK_IN": 400,
                 "ROOM_NOT_FOUND": 404,
                 "RESERVATION_CONFLICT": 409,
                 "SERVICES_NOT_ALLOWED": 400,
                 "SERVICE_NOT_FOUND": 404,
                 "DUPLICATE_SERVICES": 400,
            }
            return error_response(err, code, status_map.get(code, 400))

        # Send modification notification
        user = User.query.get(owner_id)
        NotificationService.send_notification(
            user,
            "reservation_modified",
            {
                "user_name": user.full_name,
                "pet_name": reservation.pet.name,
                "check_in_date": str(reservation.check_in_date),
                "check_out_date": str(reservation.check_out_date),
                "room_number": reservation.room.number,
            },
        )

        return success_response(
            ReservationSchema().dump(reservation),
            "Reserva actualizada exitosamente.",
        )


@blp.route("/<int:reservation_id>/status")
class ReservationStatusUpdate(MethodView):
    @admin_required
    @blp.arguments(ReservationStatusUpdateSchema)
    @blp.doc(summary="Actualizar estado de reserva", description="Admins actualizarán el estado de la reserva (inicio/fin hospedaje)")
    def patch(self, data, reservation_id):
        reservation, err, code = ReservationService.update_status(reservation_id, data)
        if err:
             status = 404 if code == "RESERVATION_NOT_FOUND" else 422 if code == "INVALID_TRANSITION" else 400
             return error_response(err, code, status)
             
        user = User.query.get(reservation.owner_id)
        
        if reservation.status == "in_progress":
             NotificationService.send_notification(
                  user,
                  "lodging_started",
                  {"user_name": user.full_name, "pet_name": reservation.pet.name}
             )
        elif reservation.status == "completed":
             NotificationService.send_notification(
                  user,
                  "lodging_ended",
                  {"user_name": user.full_name, "pet_name": reservation.pet.name}
             )
        elif reservation.status == "cancelled":
             NotificationService.send_notification(
                  user,
                  "reservation_cancelled",
                  {
                      "user_name": user.full_name,
                      "pet_name": reservation.pet.name,
                      "check_in_date": str(reservation.check_in_date),
                      "check_out_date": str(reservation.check_out_date),
                      "room_number": reservation.room.number,
                  },
             )

        return success_response(
             ReservationSchema().dump(reservation),
             "Estado de reserva actualizado exitosamente.",
        )
