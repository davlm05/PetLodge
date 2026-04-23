from datetime import date

from app.extensions import db
from app.models.pet import Pet
from app.models.reservation import Reservation


class PetService:

    @staticmethod
    def create_pet(owner_id, data):
        photo_base64 = data.pop("photo_base64", None)
        pet = Pet(owner_id=owner_id, **data)
        
        if photo_base64:
            from app.utils.image_utils import save_base64_image
            url = save_base64_image(photo_base64)
            if url:
                pet.photo_url = url
                
        db.session.add(pet)
        db.session.commit()
        return pet

    @staticmethod
    def list_pets(owner_id):
        return Pet.query.filter_by(owner_id=owner_id, is_deleted=False).order_by(Pet.created_at.desc()).all()

    @staticmethod
    def get_pet(pet_id, owner_id):
        pet = Pet.query.filter_by(id=pet_id, owner_id=owner_id, is_deleted=False).first()
        if not pet:
            return None, "Mascota no encontrada.", "PET_NOT_FOUND"
        return pet, None, None

    @staticmethod
    def update_pet(pet_id, owner_id, data):
        pet = Pet.query.filter_by(id=pet_id, owner_id=owner_id, is_deleted=False).first()
        if not pet:
            return None, "Mascota no encontrada.", "PET_NOT_FOUND"

        photo_base64 = data.pop("photo_base64", None)
        if photo_base64:
            from app.utils.image_utils import save_base64_image
            url = save_base64_image(photo_base64)
            if url:
                pet.photo_url = url

        for key, value in data.items():
            setattr(pet, key, value)

        db.session.commit()
        return pet, None, None

    @staticmethod
    def delete_pet(pet_id, owner_id):
        pet = Pet.query.filter_by(id=pet_id, owner_id=owner_id, is_deleted=False).first()
        if not pet:
            return None, "Mascota no encontrada.", "PET_NOT_FOUND"

        active_reservations = Reservation.query.filter(
            Reservation.pet_id == pet_id,
            Reservation.status.in_(["confirmed", "in_progress"]),
            Reservation.check_out_date >= date.today(),
        ).first()

        if active_reservations:
            return None, "No se puede eliminar una mascota con reservas activas o futuras.", "PET_HAS_RESERVATIONS"

        pet.is_deleted = True
        db.session.commit()
        return pet, None, None
