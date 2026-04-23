from app.extensions import ma
from marshmallow import ValidationError, fields, validate, validates_schema

SPECIES_CHOICES = ["dog", "cat", "bird", "rabbit", "hamster", "reptile", "other"]
SEX_CHOICES = ["male", "female"]
SIZE_CHOICES = ["small", "medium", "large"]


class _PetSchemaBase(ma.Schema):
    name = fields.String(required=True)
    species = fields.String(
        required=True,
        validate=validate.OneOf(SPECIES_CHOICES),
    )
    breed = fields.String(allow_none=True)
    age_years = fields.Integer(
        allow_none=True,
        validate=validate.Range(min=0),
    )
    sex = fields.String(
        allow_none=True,
        validate=validate.OneOf(SEX_CHOICES),
    )
    size = fields.String(
        allow_none=True,
        validate=validate.OneOf(SIZE_CHOICES),
    )
    photo_url = fields.String(allow_none=True)
    vaccinated = fields.Boolean(allow_none=True)
    vaccination_notes = fields.String(allow_none=True)
    has_medical_conditions = fields.Boolean(allow_none=True)
    medical_conditions_notes = fields.String(allow_none=True)
    veterinarian_name = fields.String(allow_none=True)
    veterinarian_phone = fields.String(allow_none=True)
    care_notes = fields.String(allow_none=True)
    photo_base64 = fields.String(allow_none=True, load_only=True)

    @validates_schema
    def validate_conditional_notes(self, data, **kwargs):
        if data.get("vaccinated") is True and not data.get("vaccination_notes"):
            raise ValidationError(
                "vaccination_notes is required when vaccinated is true.",
                field_name="vaccination_notes",
            )

        if data.get("has_medical_conditions") is True and not data.get(
            "medical_conditions_notes"
        ):
            raise ValidationError(
                "medical_conditions_notes is required when has_medical_conditions is true.",
                field_name="medical_conditions_notes",
            )


class PetSchema(_PetSchemaBase):
    id = fields.Integer(dump_only=True)
    owner_id = fields.Integer(dump_only=True)
    is_deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PetCreateSchema(_PetSchemaBase):
    pass


class PetUpdateSchema(_PetSchemaBase):
    name = fields.String(allow_none=True)
    species = fields.String(
        allow_none=True,
        validate=validate.OneOf(SPECIES_CHOICES),
    )

class PetNoticeSchema(ma.Schema):
    notice_message = fields.String(required=True)
