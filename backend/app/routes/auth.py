from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.auth_schema import RegisterSchema, LoginSchema, ChangePasswordSchema
from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService
from app.utils.helpers import success_response, error_response

blp = Blueprint("auth", __name__, url_prefix="/api/v1/auth", description="Autenticación de usuarios")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterSchema)
    @blp.doc(
        summary="Registrar nuevo usuario",
        description="Registro de un nuevo usuario dueño de mascotas",
    )
    def post(self, data):
        user, err, code = AuthService.register(data)
        if err:
            return error_response(err, code, 409)

        # Send registration notification
        NotificationService.send_notification(
            user,
            "user_registered",
            {"user_name": user.full_name, "email": user.email},
        )

        user_data = UserSchema().dump(user)
        return success_response(user_data, "Usuario registrado exitosamente.", 201)


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.doc(summary="Iniciar sesión", description="Login con email y contraseña, retorna JWT tokens")
    def post(self, data):
        result, err, code = AuthService.login(data["email"], data["password"])
        if err:
            return error_response(err, code, 401)
        return success_response(result, "Inicio de sesión exitoso.")


@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    @blp.doc(summary="Renovar access token", description="Usa el refresh token para obtener un nuevo access token")
    def post(self):
        result, err, code = AuthService.refresh()
        if err:
            return error_response(err, code, 401)
        return success_response(result, "Token renovado exitosamente.")


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    @blp.doc(summary="Cerrar sesión", description="Invalida el token actual (blacklist)")
    def post(self):
        AuthService.logout()
        return success_response(message="Sesión cerrada exitosamente.")


@blp.route("/change-password")
class ChangePassword(MethodView):
    @jwt_required()
    @blp.arguments(ChangePasswordSchema)
    @blp.doc(summary="Cambiar contraseña", description="Cambia la contraseña del usuario autenticado")
    def put(self, data):
        user_id = int(get_jwt_identity())
        _, err, code = AuthService.change_password(
            user_id,
            data["current_password"],
            data["new_password"],
        )
        if err:
            status = 404 if code == "USER_NOT_FOUND" else 401
            return error_response(err, code, status)
        return success_response(message="Contraseña actualizada exitosamente.")

