from app.extensions import db
from app.models.user import User


class UserService:

    @staticmethod
    def get_profile(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_profile(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado.", "USER_NOT_FOUND"

        if data.get("full_name"):
            user.full_name = data["full_name"]
        if data.get("phone") is not None:
            user.phone = data["phone"]
        if data.get("address") is not None:
            user.address = data["address"]

        db.session.commit()
        return user, None, None

    @staticmethod
    def list_all_users():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def toggle_status(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado.", "USER_NOT_FOUND"

        if user.role == "admin":
            return None, "No se puede desactivar a un administrador.", "CANNOT_TOGGLE_ADMIN"

        user.is_active = not user.is_active
        db.session.commit()
        return user, None, None
