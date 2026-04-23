from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.pet import Pet
from app.models.reservation import Reservation
from app.schemas.pet_schema import PetCreateSchema, PetUpdateSchema
from app.services.pet_service import PetService


def test_create_pet(app, sample_data):
    with app.app_context():
        pet = PetService.create_pet(
            sample_data["owner_id"],
            {
                "name": "Luna",
                "species": "cat",
                "breed": "Siamese",
                "age_years": 3,
                "sex": "female",
                "size": "small",
                "photo_url": "https://example.com/luna.jpg",
                "vaccinated": True,
                "vaccination_notes": "Vacunas al dia",
                "has_medical_conditions": True,
                "medical_conditions_notes": "Alergia leve",
                "veterinarian_name": "Dra. Mora",
                "veterinarian_phone": "8888-1111",
                "care_notes": "Alimento especial por las noches",
            },
        )
        assert pet is not None
        assert pet.name == "Luna"
        assert pet.owner_id == sample_data["owner_id"]
        assert pet.sex == "female"
        assert pet.size == "small"
        assert pet.vaccinated is True
        assert pet.vaccination_notes == "Vacunas al dia"
        assert pet.has_medical_conditions is True
        assert pet.medical_conditions_notes == "Alergia leve"
        assert pet.veterinarian_name == "Dra. Mora"
        assert pet.veterinarian_phone == "8888-1111"
        assert pet.care_notes == "Alimento especial por las noches"


def test_list_pets_excludes_deleted(app, sample_data):
    with app.app_context():
        pet2 = Pet(
            owner_id=sample_data["owner_id"],
            name="Deleted",
            species="dog",
            is_deleted=True,
        )
        db.session.add(pet2)
        db.session.commit()

        pets = PetService.list_pets(sample_data["owner_id"])
        names = [p.name for p in pets]
        assert "Firulais" in names
        assert "Deleted" not in names


def test_get_pet_wrong_owner(app, sample_data):
    with app.app_context():
        pet, err, code = PetService.get_pet(
            sample_data["pet_id"], sample_data["admin_id"]
        )
        assert pet is None
        assert code == "PET_NOT_FOUND"


def test_update_pet_new_fields(app, sample_data):
    with app.app_context():
        pet, err, code = PetService.update_pet(
            sample_data["pet_id"],
            sample_data["owner_id"],
            {
                "sex": "male",
                "size": "large",
                "vaccinated": True,
                "vaccination_notes": "Esquema completo 2026",
                "has_medical_conditions": True,
                "medical_conditions_notes": "Requiere medicacion oral",
                "veterinarian_name": "Dr. Perez",
                "veterinarian_phone": "7000-1234",
                "care_notes": "Evitar ejercicio intenso",
            },
        )
        assert err is None
        assert code is None
        assert pet.sex == "male"
        assert pet.size == "large"
        assert pet.vaccinated is True
        assert pet.vaccination_notes == "Esquema completo 2026"
        assert pet.has_medical_conditions is True
        assert pet.medical_conditions_notes == "Requiere medicacion oral"
        assert pet.veterinarian_name == "Dr. Perez"
        assert pet.veterinarian_phone == "7000-1234"
        assert pet.care_notes == "Evitar ejercicio intenso"


def test_update_pet_can_clear_optional_fields(app, sample_data):
    with app.app_context():
        pet, err, code = PetService.update_pet(
            sample_data["pet_id"],
            sample_data["owner_id"],
            {
                "breed": None,
                "age_years": None,
                "sex": None,
                "size": None,
                "vaccinated": None,
                "vaccination_notes": None,
                "has_medical_conditions": None,
                "medical_conditions_notes": None,
                "veterinarian_name": None,
                "veterinarian_phone": None,
                "care_notes": None,
            },
        )

        assert err is None
        assert code is None
        assert pet.breed is None
        assert pet.age_years is None
        assert pet.sex is None
        assert pet.size is None
        assert pet.vaccinated is None
        assert pet.vaccination_notes is None
        assert pet.has_medical_conditions is None
        assert pet.medical_conditions_notes is None
        assert pet.veterinarian_name is None
        assert pet.veterinarian_phone is None
        assert pet.care_notes is None


def test_delete_pet_success(app, sample_data):
    with app.app_context():
        pet, err, code = PetService.delete_pet(
            sample_data["pet_id"], sample_data["owner_id"]
        )
        assert pet is not None
        assert pet.is_deleted is True


def test_delete_pet_with_active_reservation(app, sample_data):
    with app.app_context():
        reservation = Reservation(
            owner_id=sample_data["owner_id"],
            pet_id=sample_data["pet_id"],
            room_id=sample_data["std_room_id"],
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=5),
            lodging_type="standard",
            status="confirmed",
            total_price=60000,
        )
        db.session.add(reservation)
        db.session.commit()

        pet, err, code = PetService.delete_pet(
            sample_data["pet_id"], sample_data["owner_id"]
        )
        assert pet is None
        assert code == "PET_HAS_RESERVATIONS"


def test_pet_create_schema_requires_vaccination_notes():
    schema = PetCreateSchema()

    with pytest.raises(Exception) as exc_info:
        schema.load(
            {
                "name": "Luna",
                "species": "dog",
                "vaccinated": True,
            }
        )

    assert "vaccination_notes" in str(exc_info.value)


def test_pet_create_schema_requires_medical_condition_notes():
    schema = PetCreateSchema()

    with pytest.raises(Exception) as exc_info:
        schema.load(
            {
                "name": "Luna",
                "species": "dog",
                "has_medical_conditions": True,
            }
        )

    assert "medical_conditions_notes" in str(exc_info.value)


def test_pet_create_schema_accepts_full_payload():
    schema = PetCreateSchema()

    payload = schema.load(
        {
            "name": "Luna",
            "species": "dog",
            "breed": "Poodle",
            "age_years": 4,
            "sex": "female",
            "size": "small",
            "photo_url": "https://example.com/luna.jpg",
            "vaccinated": True,
            "vaccination_notes": "Refuerzo anual completo",
            "has_medical_conditions": True,
            "medical_conditions_notes": "Alergia alimentaria",
            "veterinarian_name": "Dr. Ruiz",
            "veterinarian_phone": "8888-7777",
            "care_notes": "Comida hipoalergenica",
        }
    )

    assert payload["species"] == "dog"
    assert payload["sex"] == "female"
    assert payload["size"] == "small"
    assert payload["vaccinated"] is True
    assert payload["has_medical_conditions"] is True


def test_pet_update_schema_allows_partial_payload():
    schema = PetUpdateSchema()

    payload = schema.load(
        {
            "size": "medium",
            "care_notes": "Actualizar alimentacion",
        }
    )

    assert payload == {
        "size": "medium",
        "care_notes": "Actualizar alimentacion",
    }
