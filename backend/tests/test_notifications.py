from app.extensions import db
from app.models.notification_template import NotificationTemplate
from app.services.notification_service import NotificationService


def test_create_template_success(app):
    with app.app_context():
        template, err, code = NotificationService.create_template({
            "event_type": "user_registered",
            "subject": "Bienvenido {{user_name}}",
            "body_html": "<h1>Hola {{user_name}}</h1><p>Tu cuenta ha sido creada.</p>",
            "variables": "user_name,email",
        })
        assert template is not None
        assert template.event_type == "user_registered"


def test_create_template_duplicate(app):
    with app.app_context():
        NotificationService.create_template({
            "event_type": "test_event",
            "subject": "Test",
            "body_html": "<p>Test</p>",
        })
        template, err, code = NotificationService.create_template({
            "event_type": "test_event",
            "subject": "Duplicate",
            "body_html": "<p>Dup</p>",
        })
        assert template is None
        assert code == "TEMPLATE_EXISTS"


def test_update_template(app):
    with app.app_context():
        t, _, _ = NotificationService.create_template({
            "event_type": "update_test",
            "subject": "Original",
            "body_html": "<p>Original</p>",
        })
        updated, err, code = NotificationService.update_template(t.id, {
            "subject": "Updated Subject",
        })
        assert updated.subject == "Updated Subject"
        assert updated.body_html == "<p>Original</p>"


def test_interpolate_variables(app):
    with app.app_context():
        result = NotificationService._interpolate(
            "Hola {{user_name}}, tu mascota {{pet_name}} tiene reserva del {{check_in_date}} al {{check_out_date}}.",
            {
                "user_name": "Juan",
                "pet_name": "Firulais",
                "check_in_date": "2026-04-15",
                "check_out_date": "2026-04-20",
            },
        )
        assert "Juan" in result
        assert "Firulais" in result
        assert "2026-04-15" in result
        assert "{{" not in result
