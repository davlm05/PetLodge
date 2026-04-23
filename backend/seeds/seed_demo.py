import os

import click

from app.extensions import db
from app.models.pet import Pet
from app.models.user import User


def seed_demo_owner():
    email = os.getenv("DEMO_OWNER_EMAIL", "cliente@petlodge.com")
    password = os.getenv("DEMO_OWNER_PASSWORD", "Cliente123")
    full_name = os.getenv("DEMO_OWNER_FULL_NAME", "Cliente Demo")
    id_number = os.getenv("DEMO_OWNER_ID_NUMBER", "1111111110")

    owner = User.query.filter_by(email=email).first()
    if not owner:
        owner = User(
            email=email,
            full_name=full_name,
            id_number=id_number,
            phone="8888-1234",
            address="San Jose",
            role="owner",
            is_active=True,
        )
        owner.set_password(password)
        db.session.add(owner)
        db.session.flush()
        click.echo(f"  Usuario demo '{email}' creado.")
    else:
        click.echo(f"  Usuario demo '{email}' ya existe, omitido.")

    existing_pet = Pet.query.filter_by(owner_id=owner.id, name="Milo", is_deleted=False).first()
    if existing_pet:
        click.echo("  Mascota demo 'Milo' ya existe, omitida.")
    else:
        pet = Pet(
            owner_id=owner.id,
            name="Milo",
            species="dog",
            breed="Mestizo",
            age_years=3,
            sex="male",
            size="medium",
            vaccinated=True,
            vaccination_notes="Vacunas al dia",
            has_medical_conditions=False,
            veterinarian_name="Dra. Rivera",
            veterinarian_phone="2222-3333",
            care_notes="Come dos veces al dia y disfruta paseos cortos.",
        )
        db.session.add(pet)
        click.echo("  Mascota demo 'Milo' creada.")

    db.session.commit()
