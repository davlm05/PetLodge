import os
import click
from app.extensions import db
from app.models.user import User


def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "admin@petlodge.com")
    password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    full_name = os.getenv("ADMIN_FULL_NAME", "Administrador PetLodge")
    id_number = os.getenv("ADMIN_ID_NUMBER", "0000000000")

    existing = User.query.filter_by(email=email).first()
    if existing:
        click.echo(f"  Admin '{email}' ya existe, omitido.")
        return

    admin = User(
        email=email,
        full_name=full_name,
        id_number=id_number,
        role="admin",
        is_active=True,
    )
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()
    click.echo(f"  Admin '{email}' creado exitosamente.")
