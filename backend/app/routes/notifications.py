from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.notification_schema import (
    NotificationSchema,
    NotificationTemplateSchema,
    NotificationTemplateCreateSchema,
    NotificationTemplateUpdateSchema,
)
from app.services.notification_service import NotificationService
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response

blp = Blueprint(
    "notifications", __name__,
    url_prefix="/api/v1/notifications",
    description="Centro de notificaciones",
)


@blp.route("/")
class NotificationList(MethodView):
    @jwt_required()
    @blp.doc(summary="Ver mis notificaciones", description="Lista el historial de notificaciones del usuario autenticado")
    def get(self):
        user_id = int(get_jwt_identity())
        notifications = NotificationService.get_user_notifications(user_id)
        return success_response(NotificationSchema(many=True).dump(notifications))


@blp.route("/templates")
class TemplateList(MethodView):
    @admin_required
    @blp.doc(summary="Ver plantillas", description="Lista todas las plantillas de notificación (solo admin)")
    def get(self):
        templates = NotificationService.list_templates()
        return success_response(NotificationTemplateSchema(many=True).dump(templates))

    @admin_required
    @blp.arguments(NotificationTemplateCreateSchema)
    @blp.doc(summary="Crear plantilla", description="Crea una nueva plantilla de notificación (solo admin)")
    def post(self, data):
        template, err, code = NotificationService.create_template(data)
        if err:
            return error_response(err, code, 409)
        return success_response(
            NotificationTemplateSchema().dump(template),
            "Plantilla creada exitosamente.",
            201,
        )


@blp.route("/templates/<int:template_id>")
class TemplateDetail(MethodView):
    @admin_required
    @blp.arguments(NotificationTemplateUpdateSchema)
    @blp.doc(summary="Editar plantilla", description="Actualiza una plantilla de notificación (solo admin)")
    def put(self, data, template_id):
        template, err, code = NotificationService.update_template(template_id, data)
        if err:
            return error_response(err, code, 404)
        return success_response(
            NotificationTemplateSchema().dump(template),
            "Plantilla actualizada exitosamente.",
        )
