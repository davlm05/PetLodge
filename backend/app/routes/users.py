from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.user_schema import UserSchema, UserUpdateSchema
from app.services.user_service import UserService
from app.utils.decorators import admin_required, owner_required
from app.utils.helpers import success_response, error_response

blp = Blueprint("users", __name__, url_prefix="/api/v1/users", description="Gestión de usuarios")


@blp.route("/me")
class UserProfile(MethodView):
    @jwt_required()
    @blp.doc(summary="Ver perfil propio", description="Obtiene los datos del usuario autenticado")
    def get(self):
        user_id = int(get_jwt_identity())
        user = UserService.get_profile(user_id)
        if not user:
            return error_response("Usuario no encontrado.", "USER_NOT_FOUND", 404)
        return success_response(UserSchema().dump(user))

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.doc(summary="Editar perfil propio", description="Actualiza datos personales del usuario autenticado")
    def put(self, data):
        user_id = int(get_jwt_identity())
        user, err, code = UserService.update_profile(user_id, data)
        if err:
            return error_response(err, code, 404)
        return success_response(UserSchema().dump(user), "Perfil actualizado exitosamente.")


@blp.route("/")
class UserList(MethodView):
    @admin_required
    @blp.doc(summary="Listar usuarios", description="Lista todos los usuarios (solo admin)")
    def get(self):
        users = UserService.list_all_users()
        return success_response(UserSchema(many=True).dump(users))


@blp.route("/<int:user_id>/toggle-status")
class UserToggleStatus(MethodView):
    @admin_required
    @blp.doc(summary="Activar/desactivar cuenta", description="Cambia el estado activo/inactivo de un usuario (solo admin)")
    def patch(self, user_id):
        user, err, code = UserService.toggle_status(user_id)
        if err:
            status = 404 if code == "USER_NOT_FOUND" else 400
            return error_response(err, code, status)
        status_text = "activada" if user.is_active else "desactivada"
        return success_response(UserSchema().dump(user), f"Cuenta {status_text} exitosamente.")
