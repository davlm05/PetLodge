from app.extensions import db
from app.models.user import User
from app.services.auth_service import AuthService


def test_register_success(app):
    with app.app_context():
        user, err, code = AuthService.register({
            "email": "new@test.com",
            "password": "password123",
            "full_name": "New User",
            "id_number": "9999999999",
        })
        assert user is not None
        assert err is None
        assert user.email == "new@test.com"
        assert user.role == "owner"
        assert user.check_password("password123")


def test_register_duplicate_email(app, sample_data):
    with app.app_context():
        user, err, code = AuthService.register({
            "email": "owner@test.com",
            "password": "password123",
            "full_name": "Duplicate",
            "id_number": "5555555555",
        })
        assert user is None
        assert code == "EMAIL_EXISTS"


def test_register_duplicate_id_number(app, sample_data):
    with app.app_context():
        user, err, code = AuthService.register({
            "email": "other@test.com",
            "password": "password123",
            "full_name": "Duplicate ID",
            "id_number": "1111111111",
        })
        assert user is None
        assert code == "ID_EXISTS"


def test_login_success(app, sample_data):
    with app.app_context():
        result, err, code = AuthService.login("owner@test.com", "password123")
        assert result is not None
        assert err is None
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["user"]["role"] == "owner"


def test_login_invalid_credentials(app, sample_data):
    with app.app_context():
        result, err, code = AuthService.login("owner@test.com", "wrongpassword")
        assert result is None
        assert code == "INVALID_CREDENTIALS"


def test_login_disabled_account(app, sample_data):
    with app.app_context():
        user = User.query.filter_by(email="owner@test.com").first()
        user.is_active = False
        db.session.commit()

        result, err, code = AuthService.login("owner@test.com", "password123")
        assert result is None
        assert code == "ACCOUNT_DISABLED"
