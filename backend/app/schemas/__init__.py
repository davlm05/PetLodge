from app.schemas.common import SuccessResponseSchema, ErrorResponseSchema
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.schemas.user_schema import UserSchema, UserUpdateSchema
from app.schemas.pet_schema import PetSchema, PetCreateSchema, PetUpdateSchema
from app.schemas.reservation_schema import (
    ReservationSchema,
    ReservationCreateSchema,
    ReservationServiceSchema,
)
from app.schemas.notification_schema import (
    NotificationSchema,
    NotificationTemplateSchema,
    NotificationTemplateCreateSchema,
    NotificationTemplateUpdateSchema,
)
from app.schemas.catalog_schema import RoomSchema, ServiceSchema

__all__ = [
    "SuccessResponseSchema",
    "ErrorResponseSchema",
    "RegisterSchema",
    "LoginSchema",
    "UserSchema",
    "UserUpdateSchema",
    "PetSchema",
    "PetCreateSchema",
    "PetUpdateSchema",
    "ReservationSchema",
    "ReservationCreateSchema",
    "ReservationServiceSchema",
    "NotificationSchema",
    "NotificationTemplateSchema",
    "NotificationTemplateCreateSchema",
    "NotificationTemplateUpdateSchema",
    "RoomSchema",
    "ServiceSchema",
]
