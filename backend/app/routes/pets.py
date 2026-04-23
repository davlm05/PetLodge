from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.pet_schema import (
    PetCreateSchema, 
    PetSchema, 
    PetUpdateSchema,
    PetNoticeSchema
)
from app.services.pet_service import PetService
from app.services.notification_service import NotificationService
from app.models.user import User
from app.models.pet import Pet
from app.utils.helpers import error_response, success_response

blp = Blueprint(
    "pets",
    __name__,
    url_prefix="/api/v1/pets",
    description="Gestión de mascotas",
)


@blp.route("/")
class PetList(MethodView):
    @jwt_required()
    @blp.arguments(PetCreateSchema)
    @blp.doc(
        summary="Registrar mascota",
        description="Registra una nueva mascota para el dueño autenticado",
    )
    def post(self, data):
        owner_id = int(get_jwt_identity())
        pet = PetService.create_pet(owner_id, data)
        return success_response(PetSchema().dump(pet), "Mascota registrada exitosamente.", 201)

    @jwt_required()
    @blp.doc(
        summary="Listar mis mascotas",
        description="Lista todas las mascotas del dueño autenticado",
    )
    def get(self):
        owner_id = int(get_jwt_identity())
        pets = PetService.list_pets(owner_id)
        return success_response(PetSchema(many=True).dump(pets))


@blp.route("/<int:pet_id>")
class PetDetail(MethodView):
    @jwt_required()
    @blp.doc(
        summary="Ver detalle de mascota",
        description="Obtiene los datos de una mascota específica",
    )
    def get(self, pet_id):
        owner_id = int(get_jwt_identity())
        pet, err, code = PetService.get_pet(pet_id, owner_id)
        if err:
            return error_response(err, code, 404)
        return success_response(PetSchema().dump(pet))

    @jwt_required()
    @blp.arguments(PetUpdateSchema)
    @blp.doc(summary="Editar mascota", description="Actualiza los datos de una mascota")
    def put(self, data, pet_id):
        owner_id = int(get_jwt_identity())
        pet, err, code = PetService.update_pet(pet_id, owner_id, data)
        if err:
            return error_response(err, code, 404)
        return success_response(PetSchema().dump(pet), "Mascota actualizada exitosamente.")

    @jwt_required()
    @blp.doc(
        summary="Eliminar mascota",
        description="Soft delete de una mascota (no permitido si tiene reservas activas)",
    )
    def delete(self, pet_id):
        owner_id = int(get_jwt_identity())
        pet, err, code = PetService.delete_pet(pet_id, owner_id)
        if err:
            status = 404 if code == "PET_NOT_FOUND" else 409
            return error_response(err, code, status)
        return success_response(message="Mascota eliminada exitosamente.")


@blp.route("/<int:pet_id>/notices")
class PetNotice(MethodView):
    @jwt_required()
    @blp.arguments(PetNoticeSchema)
    @blp.doc(summary="Enviar aviso sobre mascota", description="Avisa al dueño sobre el estado de su mascota")
    def post(self, data, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet or pet.is_deleted:
            return error_response("Mascota no encontrada.", "PET_NOT_FOUND", 404)
            
        user = User.query.get(pet.owner_id)
        NotificationService.send_notification(
             user,
             "pet_status_notice",
             {
                  "user_name": user.full_name,
                  "pet_name": pet.name,
                  "notice_message": data["notice_message"]
             }
        )
        
        return success_response(message="Notificación enviada exitosamente.")
