import click
from flask import Flask, jsonify

from app.config import config_by_name
from app.extensions import db, migrate, jwt, mail, bcrypt, ma


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # Import models so they are registered with SQLAlchemy
    from app import models  # noqa: F401

    # JWT token blocklist check
    from app.models.token_blocklist import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(success=False, error="Token revocado.", code="TOKEN_REVOKED"), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(success=False, error="Token expirado.", code="TOKEN_EXPIRED"), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(success=False, error="Token inválido.", code="INVALID_TOKEN"), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(success=False, error="Token de autorización requerido.", code="MISSING_TOKEN"), 401

    # Register blueprints with flask-smorest API
    from flask_smorest import Api

    api = Api(app)

    from app.routes.auth import blp as auth_blp
    from app.routes.users import blp as users_blp
    from app.routes.pets import blp as pets_blp
    from app.routes.reservations import blp as reservations_blp
    from app.routes.notifications import blp as notifications_blp
    from app.routes.catalog import blp as catalog_blp

    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(pets_blp)
    api.register_blueprint(reservations_blp)
    api.register_blueprint(notifications_blp)
    api.register_blueprint(catalog_blp)

    # Register CLI commands
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    @app.cli.command("seed")
    def seed():
        """Poblar la base de datos con datos iniciales."""
        from seeds.seed_rooms import seed_rooms
        from seeds.seed_admin import seed_admin
        from seeds.seed_demo import seed_demo_owner
        from seeds.seed_templates import seed_templates

        seed_rooms()
        seed_admin()
        seed_demo_owner()
        seed_templates()
        click.echo("Seed completado.")

    @app.cli.command("seed-rooms")
    def seed_rooms_cmd():
        """Poblar habitaciones iniciales."""
        from seeds.seed_rooms import seed_rooms
        seed_rooms()
        click.echo("Habitaciones creadas.")

    @app.cli.command("seed-admin")
    def seed_admin_cmd():
        """Crear usuario administrador por defecto."""
        from seeds.seed_admin import seed_admin
        seed_admin()
        click.echo("Admin creado.")

    @app.cli.command("seed-demo")
    def seed_demo_cmd():
        """Crear usuario demo para la app movil."""
        from seeds.seed_demo import seed_demo_owner
        seed_demo_owner()
        click.echo("Demo movil creado.")
