from flask.views import MethodView
from flask_smorest import Blueprint

from app.models.room import Room
from app.models.service import Service
from app.schemas.catalog_schema import RoomSchema, ServiceSchema
from app.utils.helpers import success_response

blp = Blueprint(
    "catalog",
    __name__,
    url_prefix="/api/v1",
    description="Catalogo publico para la app movil",
)


@blp.route("/rooms")
class RoomList(MethodView):
    @blp.doc(
        summary="Listar habitaciones activas",
        description="Lista las habitaciones disponibles para crear reservas desde la app movil",
    )
    def get(self):
        rooms = Room.query.filter_by(is_active=True).order_by(Room.number.asc()).all()
        return success_response(RoomSchema(many=True).dump(rooms))


@blp.route("/services")
class ServiceList(MethodView):
    @blp.doc(
        summary="Listar servicios activos",
        description="Lista los servicios adicionales disponibles para hospedaje especial",
    )
    def get(self):
        services = Service.query.filter_by(is_active=True).order_by(Service.name.asc()).all()
        return success_response(ServiceSchema(many=True).dump(services))
