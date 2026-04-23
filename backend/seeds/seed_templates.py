from app.extensions import db
from app.models.notification_template import NotificationTemplate
from sqlalchemy.exc import IntegrityError


def seed_templates():
    templates_data = [
        {
            "event_type": "user_registered",
            "subject": "¡Bienvenido a PetLodge!",
            "body_html": "<p>Hola {{user_name}},</p><p>Gracias por registrarte en PetLodge. Ahora puedes comenzar a registrar a tus mascotas y gestionar sus reservas de hospedaje.</p><p>¡Te esperamos!</p>",
            "variables": "user_name,email",
        },
        {
            "event_type": "reservation_confirmed",
            "subject": "Confirmación de Reserva",
            "body_html": "<p>Hola {{user_name}},</p><p>Tu reserva para <b>{{pet_name}}</b> ha sido confirmada.</p><p><b>Ingreso:</b> {{check_in_date}}<br><b>Salida:</b> {{check_out_date}}<br><b>Habitación:</b> {{room_number}}</p><p>Gracias por confiar en nosotros.</p>",
            "variables": "user_name,pet_name,check_in_date,check_out_date,room_number",
        },
        {
            "event_type": "reservation_modified",
            "subject": "Actualización de tu Reserva",
            "body_html": "<p>Hola {{user_name}},</p><p>Tu reserva para <b>{{pet_name}}</b> ha sido modificada.</p><p><b>Nuevas fechas:</b> {{check_in_date}} al {{check_out_date}}<br><b>Habitación:</b> {{room_number}}</p><p>Si tienes alguna consulta, no dudes en contactarnos.</p>",
            "variables": "user_name,pet_name,check_in_date,check_out_date,room_number",
        },
        {
            "event_type": "lodging_started",
            "subject": "¡El hospedaje de tu mascota ha comenzado!",
            "body_html": "<p>Hola {{user_name}},</p><p>Te informamos que <b>{{pet_name}}</b> ya ha ingresado a nuestra instalación y su hospedaje ha comenzado.</p><p>Puedes estar tranquilo(a), ¡lo(a) cuidaremos mucho!</p>",
            "variables": "user_name,pet_name",
        },
        {
            "event_type": "lodging_ended",
            "subject": "Ha finalizado el hospedaje",
            "body_html": "<p>Hola {{user_name}},</p><p>El hospedaje de <b>{{pet_name}}</b> ha finalizado. Esperamos que haya pasado una excelente estadía con nosotros.</p><p>¡Vuelve pronto!</p>",
            "variables": "user_name,pet_name",
        },
        {
            "event_type": "reservation_cancelled",
            "subject": "Reserva cancelada",
            "body_html": "<p>Hola {{user_name}},</p><p>Tu reserva para <b>{{pet_name}}</b> ha sido cancelada.</p><p><b>Ingreso:</b> {{check_in_date}}<br><b>Salida:</b> {{check_out_date}}<br><b>Habitación:</b> {{room_number}}</p><p>Si fue un error o necesitas ayuda, no dudes en contactarnos.</p>",
            "variables": "user_name,pet_name,check_in_date,check_out_date,room_number",
        },
        {
            "event_type": "pet_status_notice",
            "subject": "Aviso sobre {{pet_name}}",
            "body_html": "<p>Hola {{user_name}},</p><p>Tenemos un aviso acerca de <b>{{pet_name}}</b>:</p><blockquote>{{notice_message}}</blockquote><p>Para más detalles, revisa la aplicación.</p>",
            "variables": "user_name,pet_name,notice_message",
        },
    ]

    count = 0
    for data in templates_data:
        existing = NotificationTemplate.query.filter_by(
            event_type=data["event_type"]
        ).first()
        if not existing:
            template = NotificationTemplate(
                event_type=data["event_type"],
                subject=data["subject"],
                body_html=data["body_html"],
                variables=data["variables"],
            )
            db.session.add(template)
            count += 1

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        pass

    print(f"Creadas {count} plantillas de notificaciones.")
