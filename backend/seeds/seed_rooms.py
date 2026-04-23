import click
from app.extensions import db
from app.models.room import Room
from app.models.service import Service


ROOMS = [
    # Standard rooms
    {"number": "E-101", "name": "Camita Cozy", "room_type": "standard", "capacity": 1, "price_per_night": 15000, "description": "Habitación estándar para mascotas pequeñas con cama acolchada."},
    {"number": "E-102", "name": "Rincón Tranquilo", "room_type": "standard", "capacity": 1, "price_per_night": 15000, "description": "Habitación estándar con ventilación natural y espacio cómodo."},
    {"number": "E-103", "name": "Nido Suave", "room_type": "standard", "capacity": 1, "price_per_night": 18000, "description": "Habitación estándar para mascotas medianas."},
    {"number": "E-104", "name": "Guarida Feliz", "room_type": "standard", "capacity": 1, "price_per_night": 18000, "description": "Habitación estándar amplia con zona de juegos."},
    {"number": "E-105", "name": "Refugio Cálido", "room_type": "standard", "capacity": 2, "price_per_night": 22000, "description": "Habitación estándar doble para dos mascotas del mismo dueño."},
    {"number": "E-106", "name": "Descanso Real", "room_type": "standard", "capacity": 2, "price_per_night": 22000, "description": "Habitación estándar doble con espacio extra."},
    # Special rooms
    {"number": "S-201", "name": "Suite Premium", "room_type": "special", "capacity": 1, "price_per_night": 30000, "description": "Suite especial con cama ortopédica, música relajante y cámara web."},
    {"number": "S-202", "name": "Suite Jardín", "room_type": "special", "capacity": 1, "price_per_night": 30000, "description": "Suite especial con acceso a jardín privado."},
    {"number": "S-203", "name": "Suite Real", "room_type": "special", "capacity": 2, "price_per_night": 40000, "description": "Suite especial doble con área de recreación y vista al parque."},
    {"number": "S-204", "name": "Suite Spa", "room_type": "special", "capacity": 1, "price_per_night": 35000, "description": "Suite especial con acceso a zona de baño y relajación."},
]

SERVICES = [
    {"name": "Baño completo", "description": "Baño con shampoo especial, secado y cepillado.", "price": 8000},
    {"name": "Paseo diario", "description": "Paseo de 30 minutos por el parque del hotel.", "price": 5000},
    {"name": "Alimentación especial", "description": "Dieta personalizada según indicaciones del dueño.", "price": 6000},
    {"name": "Sesión de juegos", "description": "Tiempo de juego supervisado con juguetes interactivos.", "price": 4000},
    {"name": "Corte de uñas", "description": "Corte y limado de uñas profesional.", "price": 3000},
    {"name": "Cepillado dental", "description": "Limpieza dental con productos especializados.", "price": 5000},
]


def seed_rooms():
    for room_data in ROOMS:
        existing = Room.query.filter_by(number=room_data["number"]).first()
        if not existing:
            room = Room(**room_data)
            db.session.add(room)
            click.echo(f"  Habitación {room_data['number']} creada.")
        else:
            click.echo(f"  Habitación {room_data['number']} ya existe, omitida.")

    for service_data in SERVICES:
        existing = Service.query.filter_by(name=service_data["name"]).first()
        if not existing:
            service = Service(**service_data)
            db.session.add(service)
            click.echo(f"  Servicio '{service_data['name']}' creado.")
        else:
            click.echo(f"  Servicio '{service_data['name']}' ya existe, omitido.")

    db.session.commit()
    click.echo("Habitaciones y servicios iniciales cargados.")
