from app.extensions import ma
from marshmallow import fields, validate, validates_schema, ValidationError

LODGING_TYPES = ["standard", "special"]


class ReservationServiceSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    service_id = fields.Integer()
    service_name = fields.String()
    quantity = fields.Integer()
    subtotal = fields.Float()


class _NestedPetSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()


class _NestedRoomSchema(ma.Schema):
    id = fields.Integer()
    number = fields.String()


class ReservationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    owner_id = fields.Integer(dump_only=True)
    pet_id = fields.Integer()
    room_id = fields.Integer()
    pet = fields.Nested(_NestedPetSchema, dump_only=True)
    room = fields.Nested(_NestedRoomSchema, dump_only=True)
    check_in_date = fields.Date()
    check_out_date = fields.Date()
    lodging_type = fields.String()
    status = fields.String()
    total_price = fields.Float()
    notes = fields.String()
    services = fields.List(fields.Nested(ReservationServiceSchema), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


MAX_STAY_DAYS = 365


class ReservationCreateSchema(ma.Schema):
    pet_id = fields.Integer(required=True)
    room_id = fields.Integer(required=True)
    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    lodging_type = fields.String(
        required=True,
        validate=validate.OneOf(LODGING_TYPES),
    )
    notes = fields.String(load_default=None)
    service_ids = fields.List(fields.Integer(), load_default=[])

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data.get("check_in_date") and data.get("check_out_date"):
            if data["check_out_date"] <= data["check_in_date"]:
                raise ValidationError(
                    "check_out_date must be after check_in_date.",
                    field_name="check_out_date",
                )
            days = (data["check_out_date"] - data["check_in_date"]).days
            if days > MAX_STAY_DAYS:
                raise ValidationError(
                    f"La estadía no puede superar {MAX_STAY_DAYS} días.",
                    field_name="check_out_date",
                )

class ReservationUpdateSchema(ma.Schema):
    room_id = fields.Integer(required=False)
    check_in_date = fields.Date(required=False)
    check_out_date = fields.Date(required=False)
    notes = fields.String(required=False)
    service_ids = fields.List(fields.Integer(), required=False)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if "check_in_date" in data and "check_out_date" in data:
            if data["check_out_date"] <= data["check_in_date"]:
                raise ValidationError(
                    "check_out_date must be after check_in_date.",
                    field_name="check_out_date",
                )
            days = (data["check_out_date"] - data["check_in_date"]).days
            if days > MAX_STAY_DAYS:
                raise ValidationError(
                    f"La estadía no puede superar {MAX_STAY_DAYS} días.",
                    field_name="check_out_date",
                )

class ReservationStatusUpdateSchema(ma.Schema):
    status = fields.String(
        required=True,
        validate=validate.OneOf(["in_progress", "completed", "cancelled"]),
    )
