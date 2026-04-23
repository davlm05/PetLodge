from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)

from app.extensions import db
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist


class AuthService:

    @staticmethod
    def register(data):
        if User.query.filter_by(email=data["email"]).first():
            return None, "El correo electrónico ya está registrado.", "EMAIL_EXISTS"

        if User.query.filter_by(id_number=data["id_number"]).first():
            return None, "El número de identificación ya está registrado.", "ID_EXISTS"

        user = User(
            email=data["email"],
            full_name=data["full_name"],
            id_number=data["id_number"],
            phone=data.get("phone"),
            address=data.get("address"),
            role="owner",
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return user, None, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "Credenciales inválidas.", "INVALID_CREDENTIALS"

        if not user.is_active:
            return None, "Cuenta desactivada. Contacte al administrador.", "ACCOUNT_DISABLED"

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
        }, None, None

    @staticmethod
    def refresh():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if not user:
            return None, "Usuario no encontrado.", "USER_NOT_FOUND"

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role},
        )
        return {"access_token": access_token}, None, None

    @staticmethod
    def logout():
        jwt_data = get_jwt()
        jti = jwt_data["jti"]
        token_type = jwt_data["type"]
        user_id = int(get_jwt_identity())

        blocked = TokenBlocklist(jti=jti, token_type=token_type, user_id=user_id)
        db.session.add(blocked)
        db.session.commit()

        return True

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado.", "USER_NOT_FOUND"

        if not user.check_password(current_password):
            return None, "La contraseña actual es incorrecta.", "INVALID_PASSWORD"

        user.set_password(new_password)
        db.session.commit()
        return user, None, None

