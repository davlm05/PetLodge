import json
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from app.extensions import db
from app.models.notification import Notification
from app.models.reservation import Reservation

BASE = "/api/v1/reservations"


def _post(client, headers, payload):
    return client.post(BASE + "/", data=json.dumps(payload), content_type="application/json", headers=headers)


def _put(client, headers, rid, payload):
    return client.put(f"{BASE}/{rid}", data=json.dumps(payload), content_type="application/json", headers=headers)


def _patch_status(client, headers, rid, payload):
    return client.patch(f"{BASE}/{rid}/status", data=json.dumps(payload), content_type="application/json", headers=headers)


def _make_payload(sample_data, **overrides):
    tomorrow = date.today() + timedelta(days=1)
    checkout = date.today() + timedelta(days=4)
    base = {
        "pet_id": sample_data["pet_id"],
        "room_id": sample_data["std_room_id"],
        "check_in_date": str(tomorrow),
        "check_out_date": str(checkout),
        "lodging_type": "standard",
    }
    base.update(overrides)
    return base


def _create_reservation(app, sample_data, **overrides):
    """Helper to insert a reservation directly in DB."""
    defaults = {
        "owner_id": sample_data["owner_id"],
        "pet_id": sample_data["pet_id"],
        "room_id": sample_data["std_room_id"],
        "check_in_date": date.today() + timedelta(days=1),
        "check_out_date": date.today() + timedelta(days=4),
        "lodging_type": "standard",
        "status": "confirmed",
        "total_price": 45000,
    }
    defaults.update(overrides)
    with app.app_context():
        r = Reservation(**defaults)
        db.session.add(r)
        db.session.commit()
        return r.id


# ── POST /api/v1/reservations/ ─────────────────────────────────────


class TestCreateReservation:

    @patch("app.services.notification_service.mail.send")
    def test_success(self, mock_send, client, sample_data, owner_headers):
        payload = _make_payload(sample_data)
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["success"] is True
        assert body["data"]["status"] == "confirmed"
        assert body["data"]["total_price"] == 15000 * 3

    @patch("app.services.notification_service.mail.send")
    def test_special_with_services(self, mock_send, client, sample_data, owner_headers):
        payload = _make_payload(
            sample_data,
            room_id=sample_data["spc_room_id"],
            lodging_type="special",
            service_ids=[sample_data["service_id"]],
        )
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 201
        body = resp.get_json()
        expected = (30000 * 3) + (8000 * 3)
        assert body["data"]["total_price"] == expected
        assert len(body["data"]["services"]) == 1

    def test_past_date(self, client, sample_data, owner_headers):
        yesterday = date.today() - timedelta(days=1)
        payload = _make_payload(sample_data, check_in_date=str(yesterday))
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "INVALID_CHECK_IN"

    def test_pet_not_found(self, client, sample_data, owner_headers):
        payload = _make_payload(sample_data, pet_id=9999)
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 404
        assert resp.get_json()["code"] == "PET_NOT_FOUND"

    def test_room_not_found(self, client, sample_data, owner_headers):
        payload = _make_payload(sample_data, room_id=9999)
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 404
        assert resp.get_json()["code"] == "ROOM_NOT_FOUND"

    @patch("app.services.notification_service.mail.send")
    def test_conflict(self, mock_send, client, app, sample_data, owner_headers):
        # Create first reservation
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        assert resp1.status_code == 201
        # Same dates + room → conflict
        payload = _make_payload(sample_data)
        resp2 = _post(client, owner_headers, payload)
        assert resp2.status_code == 409
        assert resp2.get_json()["code"] == "RESERVATION_CONFLICT"

    def test_services_not_allowed_standard(self, client, sample_data, owner_headers):
        payload = _make_payload(sample_data, service_ids=[sample_data["service_id"]])
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "SERVICES_NOT_ALLOWED"

    def test_inactive_service(self, client, sample_data, owner_headers):
        payload = _make_payload(
            sample_data,
            room_id=sample_data["spc_room_id"],
            lodging_type="special",
            service_ids=[sample_data["inactive_service_id"]],
        )
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 404
        assert resp.get_json()["code"] == "SERVICE_NOT_FOUND"

    def test_duplicate_services(self, client, sample_data, owner_headers):
        sid = sample_data["service_id"]
        payload = _make_payload(
            sample_data,
            room_id=sample_data["spc_room_id"],
            lodging_type="special",
            service_ids=[sid, sid],
        )
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "DUPLICATE_SERVICES"

    def test_no_auth(self, client, sample_data):
        payload = _make_payload(sample_data)
        resp = _post(client, {}, payload)
        assert resp.status_code == 401

    @patch("app.services.notification_service.threading.Thread")
    def test_sends_confirmation_email(self, mock_thread, client, app, sample_data, owner_headers):
        mock_thread.return_value = MagicMock()
        payload = _make_payload(sample_data)
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 201
        with app.app_context():
            notif = Notification.query.filter_by(event_type="reservation_confirmed").first()
            assert notif is not None
            assert notif.recipient_email == "owner@test.com"
        mock_thread.assert_called_once()

    def test_date_range_exceeds_365_days(self, client, sample_data, owner_headers):
        tomorrow = date.today() + timedelta(days=1)
        far_future = tomorrow + timedelta(days=400)
        payload = _make_payload(sample_data, check_in_date=str(tomorrow), check_out_date=str(far_future))
        resp = _post(client, owner_headers, payload)
        assert resp.status_code == 422  # marshmallow validation error


# ── GET /api/v1/reservations/ ──────────────────────────────────────


class TestListReservations:

    def test_empty_list(self, client, sample_data, owner_headers):
        resp = client.get(BASE + "/", headers=owner_headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"] == []

    @patch("app.services.notification_service.mail.send")
    def test_returns_own_reservations(self, mock_send, client, sample_data, owner_headers):
        _post(client, owner_headers, _make_payload(sample_data))
        resp = client.get(BASE + "/", headers=owner_headers)
        assert resp.status_code == 200
        assert len(resp.get_json()["data"]) == 1

    def test_no_auth(self, client, sample_data):
        resp = client.get(BASE + "/")
        assert resp.status_code == 401


# ── GET /api/v1/reservations/<id> ──────────────────────────────────


class TestGetReservation:

    @patch("app.services.notification_service.mail.send")
    def test_success(self, mock_send, client, sample_data, owner_headers):
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        rid = resp1.get_json()["data"]["id"]
        resp = client.get(f"{BASE}/{rid}", headers=owner_headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["id"] == rid

    def test_not_found(self, client, sample_data, owner_headers):
        resp = client.get(f"{BASE}/9999", headers=owner_headers)
        assert resp.status_code == 404

    @patch("app.services.notification_service.mail.send")
    def test_wrong_owner(self, mock_send, client, sample_data, owner_headers, other_owner_headers):
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        rid = resp1.get_json()["data"]["id"]
        resp = client.get(f"{BASE}/{rid}", headers=other_owner_headers)
        assert resp.status_code == 404


# ── DELETE /api/v1/reservations/<id> ───────────────────────────────


class TestCancelReservation:

    @patch("app.services.notification_service.mail.send")
    def test_success(self, mock_send, client, sample_data, owner_headers):
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        rid = resp1.get_json()["data"]["id"]
        resp = client.delete(f"{BASE}/{rid}", headers=owner_headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["status"] == "cancelled"

    @patch("app.services.notification_service.mail.send")
    def test_already_cancelled(self, mock_send, client, app, sample_data, owner_headers):
        rid = _create_reservation(app, sample_data, status="cancelled")
        resp = client.delete(f"{BASE}/{rid}", headers=owner_headers)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "CANNOT_CANCEL"

    @patch("app.services.notification_service.mail.send")
    def test_completed_cannot_cancel(self, mock_send, client, app, sample_data, owner_headers):
        rid = _create_reservation(app, sample_data, status="completed")
        resp = client.delete(f"{BASE}/{rid}", headers=owner_headers)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "CANNOT_CANCEL"

    def test_not_found(self, client, sample_data, owner_headers):
        resp = client.delete(f"{BASE}/9999", headers=owner_headers)
        assert resp.status_code == 404

    @patch("app.services.notification_service.threading.Thread")
    def test_sends_cancellation_email(self, mock_thread, client, app, sample_data, owner_headers):
        mock_thread.return_value = MagicMock()
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        rid = resp1.get_json()["data"]["id"]
        resp = client.delete(f"{BASE}/{rid}", headers=owner_headers)
        assert resp.status_code == 200
        with app.app_context():
            notif = Notification.query.filter_by(event_type="reservation_cancelled").first()
            assert notif is not None
            assert notif.recipient_email == "owner@test.com"


# ── PUT /api/v1/reservations/<id> ──────────────────────────────────


class TestUpdateReservation:

    @patch("app.services.notification_service.mail.send")
    def test_update_dates(self, mock_send, client, sample_data, owner_headers):
        resp1 = _post(client, owner_headers, _make_payload(sample_data))
        rid = resp1.get_json()["data"]["id"]
        new_checkin = str(date.today() + timedelta(days=5))
        new_checkout = str(date.today() + timedelta(days=8))
        resp = _put(client, owner_headers, rid, {
            "check_in_date": new_checkin,
            "check_out_date": new_checkout,
        })
        assert resp.status_code == 200
        assert resp.get_json()["data"]["check_in_date"] == new_checkin

    @patch("app.services.notification_service.mail.send")
    def test_cannot_modify_in_progress(self, mock_send, client, app, sample_data, owner_headers):
        rid = _create_reservation(app, sample_data, status="in_progress")
        resp = _put(client, owner_headers, rid, {"notes": "test"})
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "CANNOT_MODIFY"

    @patch("app.services.notification_service.mail.send")
    def test_conflict_on_update(self, mock_send, client, app, sample_data, owner_headers):
        # Create reservation occupying std_room for days 10-15
        _create_reservation(
            app, sample_data,
            check_in_date=date.today() + timedelta(days=10),
            check_out_date=date.today() + timedelta(days=15),
        )
        # Create another reservation on a different range
        resp1 = _post(client, owner_headers, _make_payload(sample_data,
            check_in_date=str(date.today() + timedelta(days=20)),
            check_out_date=str(date.today() + timedelta(days=25)),
        ))
        rid = resp1.get_json()["data"]["id"]
        # Try to move it to overlapping dates
        resp = _put(client, owner_headers, rid, {
            "check_in_date": str(date.today() + timedelta(days=11)),
            "check_out_date": str(date.today() + timedelta(days=14)),
        })
        assert resp.status_code == 409
        assert resp.get_json()["code"] == "RESERVATION_CONFLICT"


# ── PATCH /api/v1/reservations/<id>/status ─────────────────────────


class TestUpdateStatus:

    @patch("app.services.notification_service.mail.send")
    def test_to_in_progress(self, mock_send, client, app, sample_data, admin_headers):
        rid = _create_reservation(app, sample_data, status="confirmed")
        resp = _patch_status(client, admin_headers, rid, {"status": "in_progress"})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["status"] == "in_progress"

    @patch("app.services.notification_service.mail.send")
    def test_to_completed(self, mock_send, client, app, sample_data, admin_headers):
        rid = _create_reservation(app, sample_data, status="in_progress")
        resp = _patch_status(client, admin_headers, rid, {"status": "completed"})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["status"] == "completed"

    @patch("app.services.notification_service.threading.Thread")
    def test_to_cancelled_sends_email(self, mock_thread, client, app, sample_data, admin_headers):
        mock_thread.return_value = MagicMock()
        rid = _create_reservation(app, sample_data, status="confirmed")
        resp = _patch_status(client, admin_headers, rid, {"status": "cancelled"})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["status"] == "cancelled"
        with app.app_context():
            notif = Notification.query.filter_by(event_type="reservation_cancelled").first()
            assert notif is not None

    @patch("app.services.notification_service.mail.send")
    def test_invalid_transition(self, mock_send, client, app, sample_data, admin_headers):
        rid = _create_reservation(app, sample_data, status="completed")
        resp = _patch_status(client, admin_headers, rid, {"status": "in_progress"})
        assert resp.status_code == 422
        assert resp.get_json()["code"] == "INVALID_TRANSITION"

    def test_forbidden_for_owner(self, client, app, sample_data, owner_headers):
        rid = _create_reservation(app, sample_data, status="confirmed")
        resp = _patch_status(client, owner_headers, rid, {"status": "in_progress"})
        assert resp.status_code == 403

    @patch("app.services.notification_service.threading.Thread")
    def test_in_progress_sends_email(self, mock_thread, client, app, sample_data, admin_headers):
        mock_thread.return_value = MagicMock()
        rid = _create_reservation(app, sample_data, status="confirmed")
        resp = _patch_status(client, admin_headers, rid, {"status": "in_progress"})
        assert resp.status_code == 200
        with app.app_context():
            notif = Notification.query.filter_by(event_type="lodging_started").first()
            assert notif is not None
