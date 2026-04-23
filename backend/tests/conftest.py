import json
from datetime import date, timedelta

import pytest

from app import create_app
from app.extensions import db as _db
from app.models.notification_template import NotificationTemplate
from app.models.pet import Pet
from app.models.room import Room
from app.models.service import Service
from app.models.user import User


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
    yield app
    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_data(app):
    with app.app_context():
        # Owner user
        owner = User(email="owner@test.com", full_name="Owner Test", id_number="1111111111", role="owner")
        owner.set_password("password123")
        _db.session.add(owner)

        # Admin user
        admin = User(email="admin@test.com", full_name="Admin Test", id_number="2222222222", role="admin")
        admin.set_password("admin123")
        _db.session.add(admin)

        # Second owner (for wrong-owner tests)
        other = User(email="other_owner@test.com", full_name="Other Owner", id_number="3333333333", role="owner")
        other.set_password("password123")
        _db.session.add(other)
        _db.session.flush()

        # Pet
        pet = Pet(owner_id=owner.id, name="Firulais", species="dog", breed="Labrador")
        _db.session.add(pet)

        # Standard room
        std_room = Room(number="T-001", name="Test Standard", room_type="standard", price_per_night=15000)
        _db.session.add(std_room)

        # Special room
        spc_room = Room(number="T-002", name="Test Special", room_type="special", price_per_night=30000)
        _db.session.add(spc_room)

        # Active service
        service = Service(name="Baño completo", description="Baño con shampoo", price=8000)
        _db.session.add(service)

        # Inactive service
        inactive_service = Service(name="Masaje", description="Masaje relajante", price=12000, is_active=False)
        _db.session.add(inactive_service)

        # Notification templates
        for evt in [
            "reservation_confirmed",
            "reservation_modified",
            "reservation_cancelled",
            "lodging_started",
            "lodging_ended",
        ]:
            _db.session.add(NotificationTemplate(
                event_type=evt,
                subject=f"Test {evt}",
                body_html=f"<p>{{{{user_name}}}} - {evt}</p>",
                variables="user_name",
            ))

        _db.session.flush()
        _db.session.commit()

        return {
            "owner_id": owner.id,
            "admin_id": admin.id,
            "other_owner_id": other.id,
            "pet_id": pet.id,
            "std_room_id": std_room.id,
            "spc_room_id": spc_room.id,
            "service_id": service.id,
            "inactive_service_id": inactive_service.id,
        }


def _login(client, email, password):
    resp = client.post(
        "/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )
    data = resp.get_json()
    token = data["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def owner_headers(client, sample_data):
    return _login(client, "owner@test.com", "password123")


@pytest.fixture
def admin_headers(client, sample_data):
    return _login(client, "admin@test.com", "admin123")


@pytest.fixture
def other_owner_headers(client, sample_data):
    return _login(client, "other_owner@test.com", "password123")
