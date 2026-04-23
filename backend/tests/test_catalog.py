from app.extensions import db
from app.models.room import Room
from app.models.service import Service


def test_list_active_rooms(app):
    with app.app_context():
        active_room = Room(
            number="C-001",
            name="Catalog Active",
            room_type="standard",
            price_per_night=15000,
            is_active=True,
        )
        inactive_room = Room(
            number="C-002",
            name="Catalog Inactive",
            room_type="special",
            price_per_night=30000,
            is_active=False,
        )
        db.session.add_all([active_room, inactive_room])
        db.session.commit()

        response = app.test_client().get("/api/v1/rooms")
        payload = response.get_json()

        assert response.status_code == 200
        assert payload["success"] is True
        assert [room["number"] for room in payload["data"]] == ["C-001"]
        assert payload["data"][0]["price_per_night"] == 15000


def test_list_active_services(app):
    with app.app_context():
        active_service = Service(
            name="Catalog Bath",
            description="Bath service",
            price=8000,
            is_active=True,
        )
        inactive_service = Service(
            name="Catalog Hidden",
            description="Inactive service",
            price=5000,
            is_active=False,
        )
        db.session.add_all([active_service, inactive_service])
        db.session.commit()

        response = app.test_client().get("/api/v1/services")
        payload = response.get_json()

        assert response.status_code == 200
        assert payload["success"] is True
        assert [service["name"] for service in payload["data"]] == ["Catalog Bath"]
        assert payload["data"][0]["price"] == 8000
