# PetLodge - Documentacion Tecnica Completa

## Tabla de Contenidos

1. [Vision General del Proyecto](#1-vision-general-del-proyecto)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Stack Tecnologico](#3-stack-tecnologico)
4. [Backend - Capa de Configuracion](#4-backend---capa-de-configuracion)
5. [Backend - Capa de Modelos (ORM)](#5-backend---capa-de-modelos-orm)
6. [Backend - Capa de Esquemas (Validacion)](#6-backend---capa-de-esquemas-validacion)
7. [Backend - Capa de Servicios (Logica de Negocio)](#7-backend---capa-de-servicios-logica-de-negocio)
8. [Backend - Capa de Rutas (API REST)](#8-backend---capa-de-rutas-api-rest)
9. [Backend - Utilidades](#9-backend---utilidades)
10. [Backend - Seeds (Datos Iniciales)](#10-backend---seeds-datos-iniciales)
11. [Backend - Sistema de Notificaciones](#11-backend---sistema-de-notificaciones)
12. [Android App - Arquitectura](#12-android-app---arquitectura)
13. [Android App - Capa de Datos](#13-android-app---capa-de-datos)
14. [Android App - Pantallas (Activities)](#14-android-app---pantallas-activities)
15. [Diagrama Entidad-Relacion](#15-diagrama-entidad-relacion)
16. [Flujos de Negocio](#16-flujos-de-negocio)
17. [Despliegue con Docker](#17-despliegue-con-docker)
18. [Decisiones de Diseno](#18-decisiones-de-diseno)

---

## 1. Vision General del Proyecto

**PetLodge** es un sistema completo de gestion de hotel para mascotas que permite a los duenos registrar sus mascotas, crear reservas de hospedaje y recibir notificaciones por correo electronico sobre el estado de sus mascotas.

El sistema se compone de:
- **Backend**: API REST construida con Flask (Python)
- **App Movil**: Aplicacion Android nativa en Kotlin
- **Base de Datos**: PostgreSQL (produccion) / SQLite (desarrollo)

### Roles de Usuario

| Rol | Descripcion | Permisos |
|-----|------------|----------|
| `owner` | Dueno de mascotas | Registrar mascotas, crear/cancelar/modificar reservas, ver notificaciones, editar perfil |
| `admin` | Administrador del hotel | Todo lo del owner + gestionar usuarios, cambiar estados de reservas, gestionar plantillas de notificacion |

---

## 2. Arquitectura del Sistema

```
PetLodge/
├── backend/                          # API REST Flask
│   ├── app/
│   │   ├── __init__.py              # App Factory + registro de blueprints
│   │   ├── config.py                # Configuracion por ambiente
│   │   ├── extensions.py            # Instancias de extensiones Flask
│   │   ├── models/                  # Modelos SQLAlchemy (ORM)
│   │   │   ├── user.py
│   │   │   ├── pet.py
│   │   │   ├── room.py
│   │   │   ├── reservation.py
│   │   │   ├── reservation_service.py
│   │   │   ├── service.py
│   │   │   ├── notification.py
│   │   │   ├── notification_template.py
│   │   │   └── token_blocklist.py
│   │   ├── schemas/                 # Esquemas Marshmallow (validacion/serializacion)
│   │   │   ├── auth_schema.py
│   │   │   ├── pet_schema.py
│   │   │   ├── reservation_schema.py
│   │   │   ├── user_schema.py
│   │   │   ├── notification_schema.py
│   │   │   └── catalog_schema.py
│   │   ├── services/                # Logica de negocio
│   │   │   ├── auth_service.py
│   │   │   ├── pet_service.py
│   │   │   ├── reservation_service.py
│   │   │   ├── user_service.py
│   │   │   └── notification_service.py
│   │   ├── routes/                  # Endpoints de la API
│   │   │   ├── auth.py
│   │   │   ├── pets.py
│   │   │   ├── reservations.py
│   │   │   ├── users.py
│   │   │   ├── notifications.py
│   │   │   └── catalog.py
│   │   └── utils/                   # Utilidades
│   │       ├── decorators.py
│   │       ├── helpers.py
│   │       └── image_utils.py
│   ├── migrations/                  # Migraciones Alembic
│   ├── seeds/                       # Datos iniciales
│   ├── tests/                       # Tests unitarios/integracion
│   ├── requirements.txt
│   ├── run.py
│   └── docker-compose.yml
├── android-app/                     # App movil Android (Kotlin)
│   └── app/src/main/java/com/example/petlodge/
│       ├── *Activity.kt             # Pantallas
│       └── data/                    # Capa de datos
│           ├── ApiClient.kt
│           ├── PetLodgeApiService.kt
│           ├── SessionManager.kt
│           └── dto/                 # Data Transfer Objects
└── web-app/                         # Placeholder (vacio)
```

### Patron Arquitectonico del Backend

El backend sigue una arquitectura en **4 capas**:

```
[Cliente Android/Web]
        │
        ▼
┌─────────────────────┐
│   Rutas (Routes)    │  ← Recibe HTTP requests, delega a servicios
├─────────────────────┤
│ Esquemas (Schemas)  │  ← Valida y serializa datos de entrada/salida
├─────────────────────┤
│ Servicios (Services)│  ← Logica de negocio pura
├─────────────────────┤
│  Modelos (Models)   │  ← Mapeo ORM a tablas de la BD
├─────────────────────┤
│   Base de Datos     │  ← PostgreSQL / SQLite
└─────────────────────┘
```

---

## 3. Stack Tecnologico

### Backend

| Tecnologia | Version | Proposito |
|-----------|---------|-----------|
| Python | 3.x | Lenguaje principal |
| Flask | 3.1.0 | Framework web |
| SQLAlchemy + Flask-SQLAlchemy | - | ORM |
| Flask-Migrate (Alembic) | - | Migraciones de BD |
| Flask-JWT-Extended | - | Autenticacion JWT |
| Flask-Bcrypt | - | Hash de contrasenas |
| Marshmallow + Flask-Marshmallow | - | Validacion y serializacion |
| Flask-Smorest | - | Documentacion OpenAPI/Swagger |
| Flask-Mail | - | Envio de correos SMTP |
| PostgreSQL | 16 | BD en produccion |
| SQLite | - | BD en desarrollo |
| Gunicorn | - | Servidor WSGI produccion |
| Docker + Docker Compose | - | Contenedorizacion |

### Android

| Tecnologia | Proposito |
|-----------|-----------|
| Kotlin | Lenguaje principal |
| Retrofit2 | Cliente HTTP |
| OkHttp3 | Interceptores HTTP |
| Gson | Serializacion JSON |
| Glide | Carga de imagenes |
| SharedPreferences | Persistencia de sesion |
| Min SDK 24 / Target SDK 36 | Compatibilidad |

---

## 4. Backend - Capa de Configuracion

### App Factory (`app/__init__.py`)

La aplicacion usa el patron **Application Factory** de Flask:

```python
def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    # Inicializa extensiones: db, migrate, jwt, mail, bcrypt, ma
    # Registra JWT callbacks (token revocado, expirado, invalido, faltante)
    # Registra 6 blueprints via flask-smorest Api
    # Registra comandos CLI (seed, seed-rooms, seed-admin, seed-demo)
    return app
```

### Extensiones (`app/extensions.py`)

Todas las extensiones de Flask se instancian como singletons:

| Extension | Variable | Funcion |
|-----------|----------|---------|
| `Flask-SQLAlchemy` | `db` | ORM para la base de datos |
| `Flask-Migrate` | `migrate` | Migraciones con Alembic |
| `Flask-JWT-Extended` | `jwt` | Manejo de tokens JWT |
| `Flask-Mail` | `mail` | Envio de correos electronicos |
| `Flask-Bcrypt` | `bcrypt` | Hash seguro de contrasenas |
| `Flask-Marshmallow` | `ma` | Validacion/serializacion |

### Configuracion (`app/config.py`)

| Variable | Valor | Descripcion |
|----------|-------|-------------|
| `JWT_ACCESS_TOKEN_EXPIRES` | 1 hora | Duracion del access token |
| `JWT_REFRESH_TOKEN_EXPIRES` | 30 dias | Duracion del refresh token |
| `OPENAPI_URL_PREFIX` | `/api/v1` | Prefijo base de la API |
| `OPENAPI_SWAGGER_UI_PATH` | `/docs` | Ruta de la documentacion Swagger |
| `MAIL_SERVER` | `smtp.gmail.com` | Servidor SMTP |
| `MAIL_PORT` | 587 | Puerto SMTP con TLS |

**Ambientes disponibles:**

| Ambiente | Clase | BD |
|----------|-------|----|
| `development` | `DevelopmentConfig` | SQLite (`petlodge_dev.db`) |
| `production` | `ProductionConfig` | PostgreSQL (via `DATABASE_URL`) |
| `testing` | `TestingConfig` | SQLite (`petlodge_test.db`), tokens de 5 min |

### JWT Callbacks

El `__init__.py` registra callbacks para manejar errores JWT de forma estandarizada:

| Callback | Codigo | Respuesta |
|----------|--------|-----------|
| `token_in_blocklist_loader` | - | Verifica si el token esta revocado en `TokenBlocklist` |
| `revoked_token_loader` | `TOKEN_REVOKED` | 401 - Token revocado |
| `expired_token_loader` | `TOKEN_EXPIRED` | 401 - Token expirado |
| `invalid_token_loader` | `INVALID_TOKEN` | 401 - Token invalido |
| `unauthorized_loader` | `MISSING_TOKEN` | 401 - Token requerido |

---

## 5. Backend - Capa de Modelos (ORM)

### 5.1 User (tabla `users`)

Representa a los usuarios del sistema (duenos y administradores).

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador unico |
| `email` | String(120) | UNIQUE, NOT NULL, INDEX | Correo electronico |
| `password_hash` | String(255) | NOT NULL | Contrasena hasheada con bcrypt |
| `full_name` | String(150) | NOT NULL | Nombre completo |
| `id_number` | String(20) | UNIQUE, NOT NULL | Numero de identificacion (cedula) |
| `phone` | String(20) | NULLABLE | Telefono |
| `address` | Text | NULLABLE | Direccion |
| `role` | String(10) | NOT NULL, default="owner" | Rol: `owner` o `admin` |
| `is_active` | Boolean | default=True | Si la cuenta esta activa |
| `created_at` | DateTime | NOT NULL | Fecha de creacion (UTC) |
| `updated_at` | DateTime | NOT NULL, onupdate | Fecha de ultima actualizacion |

**Relaciones:**
- `pets` → uno a muchos con `Pet`
- `reservations` → uno a muchos con `Reservation`
- `notifications` → uno a muchos con `Notification`

**Metodos:**
- `set_password(password)` → hashea con bcrypt y almacena en `password_hash`
- `check_password(password)` → verifica contrasena contra el hash

### 5.2 Pet (tabla `pets`)

Representa una mascota registrada por un dueno.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `owner_id` | Integer | FK → users.id, NOT NULL | Dueno de la mascota |
| `name` | String(100) | NOT NULL | Nombre de la mascota |
| `species` | String(50) | NOT NULL | Especie (dog, cat, bird, rabbit, hamster, reptile, other) |
| `breed` | String(100) | NULLABLE | Raza |
| `age_years` | Integer | NULLABLE | Edad en anos |
| `sex` | String(20) | NULLABLE | Sexo (male, female) |
| `size` | String(20) | NULLABLE | Tamano (small, medium, large) |
| `photo_url` | String(500) | NULLABLE | URL de la foto (ruta en /static/uploads/) |
| `vaccinated` | Boolean | NULLABLE | Si esta vacunado |
| `vaccination_notes` | Text | NULLABLE | Notas de vacunacion (requerido si vaccinated=true) |
| `has_medical_conditions` | Boolean | NULLABLE | Si tiene condiciones medicas |
| `medical_conditions_notes` | Text | NULLABLE | Notas medicas (requerido si has_medical_conditions=true) |
| `veterinarian_name` | String(150) | NULLABLE | Nombre del veterinario |
| `veterinarian_phone` | String(20) | NULLABLE | Telefono del veterinario |
| `care_notes` | Text | NULLABLE | Instrucciones especiales de cuidado |
| `is_deleted` | Boolean | default=False | Soft delete |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |
| `updated_at` | DateTime | NOT NULL | Fecha de actualizacion |

**Relaciones:**
- `owner` → muchos a uno con `User`
- `reservations` → uno a muchos con `Reservation`

### 5.3 Room (tabla `rooms`)

Representa una habitacion del hotel.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `number` | String(20) | UNIQUE, NOT NULL | Numero de habitacion (ej: E-101, S-201) |
| `name` | String(100) | NOT NULL | Nombre descriptivo |
| `room_type` | String(20) | NOT NULL | Tipo: `standard` o `special` |
| `capacity` | Integer | default=1 | Capacidad de mascotas |
| `price_per_night` | Float | NOT NULL | Precio por noche (CRC) |
| `description` | Text | NULLABLE | Descripcion de la habitacion |
| `is_active` | Boolean | default=True | Si esta disponible |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |
| `updated_at` | DateTime | NOT NULL | Fecha de actualizacion |

**Relaciones:**
- `reservations` → uno a muchos con `Reservation`

### 5.4 Reservation (tabla `reservations`)

Representa una reserva de hospedaje.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `owner_id` | Integer | FK → users.id, NOT NULL, INDEX | Dueno que hizo la reserva |
| `pet_id` | Integer | FK → pets.id, NOT NULL, INDEX | Mascota hospedada |
| `room_id` | Integer | FK → rooms.id, NOT NULL, INDEX | Habitacion asignada |
| `check_in_date` | Date | NOT NULL, INDEX | Fecha de ingreso |
| `check_out_date` | Date | NOT NULL, INDEX | Fecha de salida |
| `lodging_type` | String(20) | NOT NULL | Tipo: `standard` o `special` |
| `status` | String(20) | NOT NULL, default="confirmed", INDEX | Estado actual |
| `total_price` | Float | NULLABLE | Precio total calculado |
| `notes` | Text | NULLABLE | Notas adicionales |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |
| `updated_at` | DateTime | NOT NULL | Fecha de actualizacion |

**Estados posibles de una reserva:**
```
confirmed → in_progress → completed
    │            │
    └────────────┴──────→ cancelled
```

**Relaciones:**
- `owner` → muchos a uno con `User`
- `pet` → muchos a uno con `Pet`
- `room` → muchos a uno con `Room`
- `services` → uno a muchos con `ReservationService`

### 5.5 Service (tabla `services`)

Servicios adicionales disponibles para hospedaje especial.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `name` | String(100) | UNIQUE, NOT NULL | Nombre del servicio |
| `description` | Text | NULLABLE | Descripcion |
| `price` | Float | NOT NULL | Precio por noche (CRC) |
| `is_active` | Boolean | default=True | Si esta disponible |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |
| `updated_at` | DateTime | NOT NULL | Fecha de actualizacion |

### 5.6 ReservationService (tabla `reservation_services`)

Tabla intermedia que vincula reservas con servicios adicionales.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `reservation_id` | Integer | FK → reservations.id, UNIQUE(reservation_id, service_id) | Reserva asociada |
| `service_id` | Integer | FK → services.id | Servicio contratado |
| `quantity` | Integer | NOT NULL, default=1 | Cantidad |
| `subtotal` | Float | NOT NULL | Subtotal = precio_servicio x num_noches |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |

**Propiedad computada:**
- `service_name` → retorna el nombre del servicio asociado

### 5.7 NotificationTemplate (tabla `notification_templates`)

Plantillas de correo electronico para eventos del sistema.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `event_type` | String(50) | UNIQUE, NOT NULL | Tipo de evento |
| `subject` | String(255) | NOT NULL | Asunto del correo |
| `body_html` | Text | NOT NULL | Cuerpo HTML con variables `{{variable}}` |
| `variables` | Text | NULLABLE | Lista de variables disponibles |
| `is_active` | Boolean | default=True | Si la plantilla esta activa |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |
| `updated_at` | DateTime | NOT NULL | Fecha de actualizacion |

### 5.8 Notification (tabla `notifications`)

Historial de notificaciones enviadas.

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `user_id` | Integer | FK → users.id, INDEX | Destinatario |
| `template_id` | Integer | FK → notification_templates.id, NULLABLE | Plantilla usada |
| `event_type` | String(50) | NOT NULL, INDEX | Tipo de evento |
| `subject` | String(255) | NULLABLE | Asunto renderizado |
| `body_html` | Text | NULLABLE | Cuerpo HTML renderizado |
| `recipient_email` | String(120) | NOT NULL | Email del destinatario |
| `status` | String(20) | NOT NULL, default="pending" | Estado: `pending`, `sent`, `failed` |
| `error_message` | Text | NULLABLE | Mensaje de error si fallo |
| `sent_at` | DateTime | NULLABLE | Fecha de envio exitoso |
| `created_at` | DateTime | NOT NULL | Fecha de creacion |

### 5.9 TokenBlocklist (tabla `token_blocklist`)

Almacena tokens JWT revocados (logout).

| Campo | Tipo | Restricciones | Descripcion |
|-------|------|---------------|-------------|
| `id` | Integer | PK | Identificador unico |
| `jti` | String(36) | UNIQUE, NOT NULL, INDEX | Identificador unico del token JWT |
| `token_type` | String(10) | NOT NULL | Tipo: `access` o `refresh` |
| `user_id` | Integer | FK → users.id | Usuario que cerro sesion |
| `created_at` | DateTime | NOT NULL | Fecha de revocacion |

---

## 6. Backend - Capa de Esquemas (Validacion)

Los esquemas usan **Marshmallow** para validar datos de entrada (load) y serializar datos de salida (dump).

### 6.1 Auth Schemas (`schemas/auth_schema.py`)

**RegisterSchema** (entrada para registro):
- `email` — String, requerido
- `password` — String, requerido, minimo 8 caracteres
- `full_name` — String, requerido
- `id_number` — String, requerido
- `phone` — String, opcional
- `address` — String, opcional

**LoginSchema** (entrada para login):
- `email` — String, requerido
- `password` — String, requerido

**ChangePasswordSchema**:
- `current_password` — String, requerido
- `new_password` — String, requerido, minimo 8 caracteres

### 6.2 Pet Schemas (`schemas/pet_schema.py`)

**PetCreateSchema** (entrada para crear mascota):
- `name` — String, requerido
- `species` — String, requerido, valores: `dog`, `cat`, `bird`, `rabbit`, `hamster`, `reptile`, `other`
- `breed` — String, opcional
- `age_years` — Integer, opcional, minimo 0
- `sex` — String, opcional, valores: `male`, `female`
- `size` — String, opcional, valores: `small`, `medium`, `large`
- `photo_base64` — String, opcional, solo carga (no se serializa en respuesta)
- `vaccinated` — Boolean, opcional
- `vaccination_notes` — String, opcional (requerido si `vaccinated=true`)
- `has_medical_conditions` — Boolean, opcional
- `medical_conditions_notes` — String, opcional (requerido si `has_medical_conditions=true`)
- `veterinarian_name`, `veterinarian_phone`, `care_notes` — Strings, opcionales

**PetUpdateSchema**: Mismos campos pero `name` y `species` son opcionales.

**PetNoticeSchema**: `notice_message` — String, requerido.

**PetSchema** (salida): Incluye todos los campos + `id`, `owner_id`, `is_deleted`, `created_at`, `updated_at`.

### 6.3 Reservation Schemas (`schemas/reservation_schema.py`)

**ReservationCreateSchema** (entrada para crear reserva):
- `pet_id` — Integer, requerido
- `room_id` — Integer, requerido
- `check_in_date` — Date, requerido
- `check_out_date` — Date, requerido
- `lodging_type` — String, requerido, valores: `standard`, `special`
- `notes` — String, opcional
- `service_ids` — Lista de Integer, default=[]

**Validacion de fechas:**
- `check_out_date` debe ser posterior a `check_in_date`
- La estadia no puede superar 365 dias

**ReservationUpdateSchema**: Todos los campos opcionales, misma validacion de fechas.

**ReservationStatusUpdateSchema**: `status` — String, requerido, valores: `in_progress`, `completed`, `cancelled`.

**ReservationSchema** (salida):
- Incluye `pet` anidado (id, name)
- Incluye `room` anidado (id, number)
- Incluye `services` como lista de `ReservationServiceSchema` (service_id, service_name, quantity, subtotal)

### 6.4 User Schemas (`schemas/user_schema.py`)

**UserSchema** (salida): `id`, `email`, `full_name`, `id_number`, `phone`, `address`, `role`, `is_active`, `created_at`.

**UserUpdateSchema** (entrada): `full_name`, `phone`, `address` — todos opcionales.

### 6.5 Notification Schemas (`schemas/notification_schema.py`)

**NotificationSchema** (salida): `id`, `event_type`, `subject`, `recipient_email`, `status`, `error_message`, `sent_at`, `created_at`.

**NotificationTemplateCreateSchema**: `event_type` (requerido), `subject`, `body_html`, `variables` (opcional).

**NotificationTemplateUpdateSchema**: Todos opcionales.

### 6.6 Catalog Schemas (`schemas/catalog_schema.py`)

**RoomSchema** (salida): `id`, `number`, `name`, `room_type`, `capacity`, `price_per_night`, `description`, `is_active`.

**ServiceSchema** (salida): `id`, `name`, `description`, `price`, `is_active`.

---

## 7. Backend - Capa de Servicios (Logica de Negocio)

### 7.1 AuthService (`services/auth_service.py`)

| Metodo | Parametros | Logica | Retorno |
|--------|-----------|--------|---------|
| `register(data)` | Datos del formulario | 1. Verifica email unico 2. Verifica id_number unico 3. Crea User con rol "owner" 4. Hashea contrasena | `(user, None, None)` o `(None, error, code)` |
| `login(email, password)` | Credenciales | 1. Busca usuario por email 2. Verifica contrasena 3. Verifica cuenta activa 4. Genera access+refresh tokens con claim `role` | `(tokens_dict, None, None)` o `(None, error, code)` |
| `refresh()` | - (usa JWT identity) | 1. Obtiene identity del refresh token 2. Genera nuevo access token | `({"access_token": ...}, None, None)` |
| `logout()` | - (usa JWT actual) | 1. Extrae JTI del token actual 2. Lo anade a `TokenBlocklist` | `True` |
| `change_password(user_id, current, new)` | ID + contrasenas | 1. Busca usuario 2. Verifica contrasena actual 3. Establece nueva contrasena | `(user, None, None)` o `(None, error, code)` |

**Codigos de error:** `EMAIL_EXISTS`, `ID_EXISTS`, `INVALID_CREDENTIALS`, `ACCOUNT_DISABLED`, `USER_NOT_FOUND`, `INVALID_PASSWORD`

### 7.2 PetService (`services/pet_service.py`)

| Metodo | Logica |
|--------|--------|
| `create_pet(owner_id, data)` | Extrae `photo_base64` de los datos. Crea Pet. Si hay foto base64, la decodifica y guarda como archivo JPEG en `/static/uploads/`. |
| `list_pets(owner_id)` | Retorna mascotas donde `is_deleted=False`, ordenadas por `created_at` desc. |
| `get_pet(pet_id, owner_id)` | Busca mascota por ID + owner_id + no eliminada. Valida propiedad. |
| `update_pet(pet_id, owner_id, data)` | Valida propiedad. Maneja actualizacion de foto. Actualiza campos dinamicamente con `setattr`. |
| `delete_pet(pet_id, owner_id)` | Valida que no tenga reservas activas/futuras (status `confirmed` o `in_progress` con `check_out_date >= today`). Marca `is_deleted=True` (soft delete). |

**Codigos de error:** `PET_NOT_FOUND`, `PET_HAS_RESERVATIONS`

### 7.3 ReservationService (`services/reservation_service.py`)

**Este es el servicio mas complejo del sistema.**

#### `check_availability(room_id, check_in, check_out, exclude_reservation_id=None)`

Verifica disponibilidad de una habitacion en un rango de fechas:
- Busca reservas existentes para esa habitacion con status `confirmed` o `in_progress`
- Detecta solapamiento: `check_in_existente < check_out_solicitado AND check_out_existente > check_in_solicitado`
- Opcionalmente excluye una reserva (para modificaciones)
- Retorna `True` si esta disponible, `False` si hay conflicto

#### `create_reservation(owner_id, data)`

Flujo completo de creacion:

1. **Valida fecha de ingreso** → no puede ser en el pasado
2. **Valida mascota** → pertenece al owner y no esta eliminada
3. **Valida habitacion** → existe y esta activa
4. **Verifica disponibilidad** → no hay solapamiento de fechas
5. **Valida servicios** → solo permitidos si `lodging_type == "special"`, sin duplicados
6. **Calcula precio total:**
   - `total = precio_habitacion * num_noches`
   - Para cada servicio: `subtotal = precio_servicio * num_noches`, se suma al total
7. **Crea registros** → `Reservation` + `ReservationService` por cada servicio
8. **Commit** → retorna la reserva creada

#### `cancel_reservation(reservation_id, owner_id)`

- Valida propiedad de la reserva
- Solo permite cancelar si el status no es `completed` ni `cancelled`
- Cambia status a `cancelled`

#### `update_reservation(reservation_id, owner_id, data)`

- Solo permite modificar reservas con status `confirmed`
- Si cambian fechas o habitacion: re-verifica disponibilidad (excluyendo la reserva actual)
- Si cambian servicios: borra los existentes y crea nuevos
- Recalcula el precio total en todos los casos

#### `update_status(reservation_id, data)` (Solo admin)

Implementa una **maquina de estados** con transiciones validas:

```
VALID_TRANSITIONS = {
    "confirmed":   ["in_progress", "cancelled"],
    "in_progress": ["completed", "cancelled"],
    "completed":   [],           # Estado final
    "cancelled":   [],           # Estado final
}
```

**Codigos de error:** `INVALID_CHECK_IN`, `PET_NOT_FOUND`, `ROOM_NOT_FOUND`, `RESERVATION_CONFLICT`, `SERVICES_NOT_ALLOWED`, `SERVICE_NOT_FOUND`, `DUPLICATE_SERVICES`, `RESERVATION_NOT_FOUND`, `CANNOT_CANCEL`, `CANNOT_MODIFY`, `INVALID_TRANSITION`

### 7.4 UserService (`services/user_service.py`)

| Metodo | Logica |
|--------|--------|
| `get_profile(user_id)` | Retorna usuario por ID |
| `update_profile(user_id, data)` | Actualiza `full_name`, `phone`, `address` |
| `list_all_users()` | Retorna todos los usuarios (admin) |
| `toggle_status(user_id)` | Invierte `is_active`. No permite desactivar admins. |

**Codigos de error:** `USER_NOT_FOUND`, `CANNOT_TOGGLE_ADMIN`

### 7.5 NotificationService (`services/notification_service.py`)

Ver seccion [11. Sistema de Notificaciones](#11-backend---sistema-de-notificaciones).

---

## 8. Backend - Capa de Rutas (API REST)

Todas las rutas usan el prefijo base `/api/v1`.

### 8.1 Autenticacion (`/api/v1/auth`)

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `POST` | `/auth/register` | No | Registra nuevo usuario (rol owner). Envia notificacion de bienvenida. |
| `POST` | `/auth/login` | No | Login con email/password. Retorna access_token + refresh_token + datos del usuario. |
| `POST` | `/auth/refresh` | Refresh Token | Genera nuevo access_token usando el refresh_token. |
| `POST` | `/auth/logout` | Access Token | Revoca el token actual (lo agrega a blocklist). |
| `PUT` | `/auth/change-password` | Access Token | Cambia la contrasena. Requiere contrasena actual. |

**Formato de respuesta del login:**
```json
{
  "success": true,
  "message": "Inicio de sesion exitoso.",
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "full_name": "Juan Perez",
      "role": "owner"
    }
  }
}
```

### 8.2 Mascotas (`/api/v1/pets`)

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `POST` | `/pets/` | JWT (owner) | Registra nueva mascota. Soporta foto en base64. |
| `GET` | `/pets/` | JWT (owner) | Lista mascotas del usuario (no eliminadas). |
| `GET` | `/pets/<id>` | JWT (owner) | Detalle de una mascota (valida propiedad). |
| `PUT` | `/pets/<id>` | JWT (owner) | Actualiza datos de la mascota. |
| `DELETE` | `/pets/<id>` | JWT (owner) | Soft delete (falla si tiene reservas activas). |
| `POST` | `/pets/<id>/notices` | JWT | Envia notificacion de estado al dueno de la mascota. |

### 8.3 Reservas (`/api/v1/reservations`)

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `POST` | `/reservations/` | JWT (owner) | Crea reserva. Valida disponibilidad, calcula precio, envia notificacion. |
| `GET` | `/reservations/` | JWT (owner) | Lista historial de reservas del usuario. |
| `GET` | `/reservations/<id>` | JWT (owner) | Detalle de una reserva (valida propiedad). |
| `PUT` | `/reservations/<id>` | JWT (owner) | Modifica reserva (solo si status=confirmed). Envia notificacion. |
| `DELETE` | `/reservations/<id>` | JWT (owner) | Cancela reserva. Envia notificacion. |
| `PATCH` | `/reservations/<id>/status` | JWT (admin) | Cambia estado de reserva (maquina de estados). Envia notificacion segun nuevo estado. |

### 8.4 Usuarios (`/api/v1/users`)

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `GET` | `/users/me` | JWT | Obtiene perfil del usuario autenticado. |
| `PUT` | `/users/me` | JWT | Actualiza perfil (full_name, phone, address). |
| `GET` | `/users/` | JWT (admin) | Lista todos los usuarios del sistema. |
| `PATCH` | `/users/<id>/toggle-status` | JWT (admin) | Activa/desactiva una cuenta de usuario. |

### 8.5 Catalogo (`/api/v1`) - Publico

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `GET` | `/rooms` | No | Lista habitaciones activas (para la app movil). |
| `GET` | `/services` | No | Lista servicios activos (para hospedaje especial). |

### 8.6 Notificaciones (`/api/v1/notifications`)

| Metodo | Ruta | Auth | Descripcion |
|--------|------|------|-------------|
| `GET` | `/notifications/` | JWT | Historial de notificaciones del usuario. |
| `GET` | `/notifications/templates` | JWT (admin) | Lista todas las plantillas. |
| `POST` | `/notifications/templates` | JWT (admin) | Crea nueva plantilla de notificacion. |
| `PUT` | `/notifications/templates/<id>` | JWT (admin) | Edita una plantilla existente. |

### Formato Estandar de Respuestas

**Exito:**
```json
{
  "success": true,
  "message": "Operacion exitosa.",
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Descripcion del error.",
  "code": "ERROR_CODE"
}
```

---

## 9. Backend - Utilidades

### 9.1 Decoradores (`utils/decorators.py`)

**`@admin_required`**
- Verifica que el JWT contenga el claim `role == "admin"`
- Retorna 403 con `code: FORBIDDEN` si no es admin
- Usa `verify_jwt_in_request()` internamente (no necesita `@jwt_required()` adicional)

**`@owner_required`**
- Verifica que el JWT contenga el claim `role == "owner"`
- Retorna 403 con `code: FORBIDDEN` si no es owner

### 9.2 Helpers (`utils/helpers.py`)

**`success_response(data=None, message="Operacion exitosa", status_code=200)`**
- Construye respuesta JSON estandarizada con `success: true`
- El campo `data` solo se incluye si no es `None`

**`error_response(error, code="ERROR", status_code=400)`**
- Construye respuesta JSON estandarizada con `success: false`

### 9.3 Image Utils (`utils/image_utils.py`)

**`save_base64_image(base64_string) → str | None`**

1. Verifica que el string no este vacio
2. Si contiene prefijo data URL (`data:image/jpeg;base64,...`), lo elimina
3. Decodifica el base64 a bytes
4. Genera nombre unico: `pet_{uuid}.jpg`
5. Guarda en `app/static/uploads/`
6. Retorna la ruta relativa `/static/uploads/pet_xxx.jpg`
7. Retorna `None` si hay error

---

## 10. Backend - Seeds (Datos Iniciales)

Los seeds se ejecutan con el comando CLI `flask seed` (o individualmente).

### 10.1 Habitaciones y Servicios (`seeds/seed_rooms.py`)

**Habitaciones Estandar (E-xxx):**

| Numero | Nombre | Capacidad | Precio/noche (CRC) |
|--------|--------|-----------|---------------------|
| E-101 | Camita Cozy | 1 | 15,000 |
| E-102 | Rincon Tranquilo | 1 | 15,000 |
| E-103 | Nido Suave | 1 | 18,000 |
| E-104 | Guarida Feliz | 1 | 18,000 |
| E-105 | Refugio Calido | 2 | 22,000 |
| E-106 | Descanso Real | 2 | 22,000 |

**Habitaciones Especiales (S-xxx):**

| Numero | Nombre | Capacidad | Precio/noche (CRC) |
|--------|--------|-----------|---------------------|
| S-201 | Suite Premium | 1 | 30,000 |
| S-202 | Suite Jardin | 1 | 30,000 |
| S-203 | Suite Real | 2 | 40,000 |
| S-204 | Suite Spa | 1 | 35,000 |

**Servicios Adicionales (solo para hospedaje especial):**

| Servicio | Precio/noche (CRC) | Descripcion |
|----------|---------------------|-------------|
| Bano completo | 8,000 | Bano con shampoo especial, secado y cepillado |
| Paseo diario | 5,000 | Paseo de 30 min por el parque del hotel |
| Alimentacion especial | 6,000 | Dieta personalizada |
| Sesion de juegos | 4,000 | Juego supervisado con juguetes interactivos |
| Corte de unas | 3,000 | Corte y limado profesional |
| Cepillado dental | 5,000 | Limpieza dental con productos especializados |

### 10.2 Admin (`seeds/seed_admin.py`)

Crea el usuario administrador por defecto con datos de variables de entorno (`ADMIN_EMAIL`, `ADMIN_PASSWORD`, etc.).

### 10.3 Demo (`seeds/seed_demo.py`)

Crea un usuario demo para pruebas de la app movil.

### 10.4 Plantillas (`seeds/seed_templates.py`)

Crea plantillas de notificacion para los 7 tipos de eventos del sistema.

---

## 11. Backend - Sistema de Notificaciones

### Flujo de una Notificacion

```
1. Evento ocurre (registro, reserva, etc.)
        │
        ▼
2. La Ruta llama a NotificationService.send_notification(user, event_type, context)
        │
        ▼
3. Se busca la plantilla activa para el event_type
        │
        ▼
4. Se interpolan las variables {{var}} en subject y body_html
        │
        ▼
5. Se crea registro Notification con status="pending"
        │
        ▼
6. Se lanza un HILO (threading.Thread) para enviar el email
        │
        ▼
7. El hilo envia el email via Flask-Mail (SMTP Gmail)
        │
        ├── Exito → status="sent", sent_at=ahora
        └── Error → status="failed", error_message=str(error)
```

### Tipos de Eventos

| event_type | Disparado cuando | Variables del contexto |
|------------|------------------|----------------------|
| `user_registered` | Un usuario se registra | `user_name`, `email` |
| `reservation_confirmed` | Se crea una reserva | `user_name`, `pet_name`, `check_in_date`, `check_out_date`, `room_number` |
| `reservation_cancelled` | Se cancela una reserva | `user_name`, `pet_name`, `check_in_date`, `check_out_date`, `room_number` |
| `reservation_modified` | Se modifica una reserva | `user_name`, `pet_name`, `check_in_date`, `check_out_date`, `room_number` |
| `lodging_started` | Admin marca como in_progress | `user_name`, `pet_name` |
| `lodging_ended` | Admin marca como completed | `user_name`, `pet_name` |
| `pet_status_notice` | Se envia aviso sobre mascota | `user_name`, `pet_name`, `notice_message` |

### Interpolacion de Variables

Las plantillas usan sintaxis `{{variable}}`. El metodo `_interpolate()` reemplaza cada `{{key}}` con el valor del contexto:

```python
def _interpolate(text, context):
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text
```

---

## 12. Android App - Arquitectura

### Estructura del Proyecto

```
com.example.petlodge/
├── PetLodgeApplication.kt        # Application class
├── LoginActivity.kt               # Pantalla de login
├── RegisterActivity.kt            # Pantalla de registro
├── MainActivity.kt                # Menu principal (hub)
├── MisMascotasActivity.kt         # Lista de mascotas
├── RegistrarMascotaActivity.kt    # Formulario nueva mascota
├── DetalleMascotaActivity.kt      # Detalle de mascota
├── EditarMascotaActivity.kt       # Editar mascota
├── CrearReservaActivity.kt        # Formulario de reserva
├── MisReservasActivity.kt         # Lista de reservas
├── NotificacionesActivity.kt      # Historial de notificaciones
├── MiPerfilActivity.kt            # Perfil del usuario
├── CambiarContraActivity.kt       # Cambiar contrasena
└── data/
    ├── ApiClient.kt               # Configuracion Retrofit
    ├── PetLodgeApiService.kt      # Definicion de endpoints
    ├── SessionManager.kt          # Persistencia de sesion
    └── dto/
        ├── AuthDtos.kt            # DTOs de autenticacion
        ├── PetDtos.kt             # DTOs de mascotas
        ├── ReservationDtos.kt     # DTOs de reservas
        ├── CatalogDtos.kt         # DTOs de catalogo
        ├── UserDtos.kt            # DTOs de usuarios
        └── NotificationDtos.kt    # DTOs de notificaciones
```

---

## 13. Android App - Capa de Datos

### 13.1 ApiClient (`data/ApiClient.kt`)

Configura la instancia singleton de Retrofit:

- **Base URL**: `http://<SERVER_IP>:5000/api/v1/` — La IP del servidor se configura en la constante `SERVER_IP` de `ApiClient.kt`. Actualmente apunta a `192.168.50.232` (dispositivo fisico en red local). Para el emulador Android se usa `10.0.2.2` (alias de localhost del host).
- **Static Base URL**: `http://<SERVER_IP>:5000/static/uploads/` (para cargar fotos de mascotas)
- **Interceptor de autenticacion**: Agrega automaticamente el header `Authorization: Bearer <token>` a cada request usando el token almacenado en `SessionManager`
- **Logging interceptor**: Registra las peticiones HTTP a nivel BASIC
- **Conversor**: Gson para serializacion/deserializacion JSON

### 13.2 SessionManager (`data/SessionManager.kt`)

Maneja la persistencia de la sesion del usuario en `SharedPreferences`:

| Dato almacenado | Clave | Descripcion |
|----------------|-------|-------------|
| `access_token` | Token de acceso JWT | Para autenticar requests |
| `refresh_token` | Token de refresco | Para renovar el access token |
| `user_id` | ID del usuario | Identificacion local |
| `full_name` | Nombre completo | Para mostrar en UI |
| `email` | Correo | Para mostrar en perfil |
| `role` | Rol del usuario | Para control de acceso local |

**Metodos principales:**
- `saveSession(loginResponse)` → Guarda todos los datos de la sesion
- `getAccessToken()` → Retorna el token de acceso
- `clearSession()` → Limpia todos los datos (logout)
- `isLoggedIn()` → Verifica si hay un token almacenado

### 13.3 PetLodgeApiService (`data/PetLodgeApiService.kt`)

Define todos los endpoints como metodos de interfaz Retrofit:

```kotlin
// Autenticacion
@POST("auth/login")      fun login(body: LoginRequest): Call<ApiResponse<LoginResponse>>
@POST("auth/register")   fun register(body: RegisterRequest): Call<ApiResponse<AuthUser>>
@PUT("auth/change-password") fun changePassword(body: ChangePasswordRequest): Call<ApiResponse<Any>>

// Perfil
@GET("users/me")          fun getProfile(): Call<ApiResponse<UserResponse>>
@PUT("users/me")           fun updateProfile(body: UserUpdateRequest): Call<ApiResponse<UserResponse>>

// Mascotas
@GET("pets/")              fun getPets(): Call<ApiResponse<List<PetResponse>>>
@POST("pets/")             fun createPet(body: PetRequest): Call<ApiResponse<PetResponse>>
@GET("pets/{id}")          fun getPetById(id: Int): Call<ApiResponse<PetResponse>>
@PUT("pets/{id}")          fun updatePet(id: Int, body: PetRequest): Call<ApiResponse<PetResponse>>
@DELETE("pets/{id}")       fun deletePet(id: Int): Call<ApiResponse<Any>>

// Catalogo (publico)
@GET("rooms")              fun getRooms(): Call<ApiResponse<List<RoomResponse>>>
@GET("services")           fun getServices(): Call<ApiResponse<List<ServiceResponse>>>

// Reservas
@GET("reservations/")      fun getReservations(): Call<ApiResponse<List<ReservationResponse>>>
@POST("reservations/")     fun createReservation(body: ReservationCreateRequest): Call<ApiResponse<ReservationResponse>>
@DELETE("reservations/{id}") fun cancelReservation(id: Int): Call<ApiResponse<Any>>

// Notificaciones
@GET("notifications/")     fun getNotifications(): Call<ApiResponse<List<NotificationResponse>>>
```

### 13.4 DTOs (Data Transfer Objects)

**ApiResponse<T>** — Wrapper generico para todas las respuestas:
```kotlin
data class ApiResponse<T>(
    val success: Boolean,
    val message: String?,
    val data: T?,
    val error: String?,
    val code: String?
)
```

**LoginResponse:**
```kotlin
data class LoginResponse(
    val access_token: String,
    val refresh_token: String,
    val user: AuthUser
)
```

**ReservationCreateRequest:**
```kotlin
data class ReservationCreateRequest(
    val pet_id: Int,
    val room_id: Int,
    val check_in_date: String,    // formato: yyyy-MM-dd
    val check_out_date: String,
    val lodging_type: String,     // "standard" o "special"
    val notes: String?,
    val service_ids: List<Int>
)
```

---

## 14. Android App - Pantallas (Activities)

### 14.1 LoginActivity

- Campos: email, contrasena
- Validacion: campos no vacios
- Al hacer login exitoso: guarda sesion con `SessionManager.saveSession()` y navega a `MainActivity`
- Enlace a `RegisterActivity` para nuevos usuarios

### 14.2 RegisterActivity

- Campos: email, contrasena, nombre completo, numero de ID, telefono (requerido, minimo 8 caracteres), direccion (opcional)
- Validacion local: telefono obligatorio con longitud minima de 8 caracteres
- Al registrar: auto-login (guarda sesion y navega a `MainActivity`)

### 14.3 MainActivity (Hub Principal)

Menu principal con botones de navegacion a:
- Mis Mascotas (`MisMascotasActivity`)
- Mis Reservas (`MisReservasActivity`)
- Crear Reserva (`CrearReservaActivity`)
- Notificaciones (`NotificacionesActivity`)
- Mi Perfil (`MiPerfilActivity`)

### 14.4 MisMascotasActivity

- Lista las mascotas del usuario en tarjetas
- Cada tarjeta muestra: foto (via Glide), nombre, especie, raza, tamano
- Botones: Ver Detalles → `DetalleMascotaActivity`, Registrar Nueva → `RegistrarMascotaActivity`
- Se refresca automaticamente al volver (`onResume`)

### 14.5 RegistrarMascotaActivity

- Formulario completo de registro de mascota
- Captura de foto: convierte a base64 para enviar al backend
- Campos condicionales: notas de vacunacion aparecen si `vaccinated=true`

### 14.6 DetalleMascotaActivity / EditarMascotaActivity

- Detalle: muestra toda la informacion de la mascota incluyendo foto, datos medicos y veterinario
- Editar: formulario pre-cargado con datos actuales, permite cambiar foto

### 14.7 CrearReservaActivity (Pantalla mas compleja)

**Flujo de la pantalla:**

1. **Carga inicial**: 3 llamadas API en paralelo para cargar mascotas, habitaciones y servicios
2. **Seleccion**: Spinners para mascota y habitacion (muestra tipo y precio)
3. **Fechas**: DatePicker para check-in y check-out con validacion (no en pasado, checkout > checkin)
4. **Servicios**: Checkboxes que solo aparecen si la habitacion es de tipo `special`
5. **Calculo de precio en tiempo real**:
   ```
   precio_total = precio_habitacion * num_noches
   + suma(precio_servicio * num_noches) para cada servicio seleccionado
   ```
6. **Envio**: Construye `ReservationCreateRequest` y envia POST a `/reservations/`

### 14.8 MisReservasActivity

- Lista de reservas ordenadas por fecha de creacion
- Cada tarjeta muestra: nombre de mascota, numero de habitacion, fechas, estado, precio total
- Boton de cancelar (llama DELETE al endpoint)

### 14.9 NotificacionesActivity

- Lista del historial de notificaciones
- Muestra: tipo de evento, asunto, estado de envio (sent/failed), fecha

### 14.10 MiPerfilActivity

- Muestra datos del usuario: nombre, email, telefono, direccion
- Permite editar: nombre, telefono, direccion
- Validacion local: telefono debe tener al menos 8 caracteres
- Boton para cambiar contrasena → `CambiarContraActivity`

### 14.11 CambiarContraActivity

- Campos: contrasena actual, nueva contrasena
- Llama PUT a `/auth/change-password`

---

## 15. Diagrama Entidad-Relacion

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │    pets     │       │    rooms    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──┐   │ id (PK)     │       │ id (PK)     │
│ email       │   │   │ owner_id(FK)│───────│ number      │
│ password_h  │   │   │ name        │       │ name        │
│ full_name   │   │   │ species     │       │ room_type   │
│ id_number   │   │   │ breed       │       │ capacity    │
│ phone       │   │   │ age_years   │       │ price_p_n   │
│ address     │   │   │ sex         │       │ description │
│ role        │   │   │ size        │       │ is_active   │
│ is_active   │   │   │ photo_url   │       └──────┬──────┘
│ created_at  │   │   │ vaccinated  │              │
│ updated_at  │   │   │ is_deleted  │              │
└──────┬──────┘   │   └──────┬──────┘              │
       │          │          │                     │
       │          │          │                     │
       │    ┌─────┴──────────┴─────────────────────┘
       │    │
       │    ▼
       │  ┌──────────────────┐       ┌─────────────────────┐
       │  │  reservations    │       │     services        │
       │  ├──────────────────┤       ├─────────────────────┤
       │  │ id (PK)          │       │ id (PK)             │
       ├──│ owner_id (FK)    │       │ name                │
          │ pet_id (FK)      │       │ description         │
          │ room_id (FK)     │       │ price               │
          │ check_in_date    │       │ is_active            │
          │ check_out_date   │       └──────────┬──────────┘
          │ lodging_type     │                  │
          │ status           │                  │
          │ total_price      │                  │
          │ notes            │                  │
          └────────┬─────────┘                  │
                   │                            │
                   ▼                            │
          ┌────────────────────────┐            │
          │  reservation_services  │            │
          ├────────────────────────┤            │
          │ id (PK)                │            │
          │ reservation_id (FK)    │            │
          │ service_id (FK)        │────────────┘
          │ quantity               │
          │ subtotal               │
          │ UNIQUE(res_id, svc_id) │
          └────────────────────────┘

┌──────────────────────────┐      ┌──────────────────────────┐
│  notification_templates  │      │     notifications       │
├──────────────────────────┤      ├──────────────────────────┤
│ id (PK)                  │◄─────│ template_id (FK)         │
│ event_type (UNIQUE)      │      │ id (PK)                  │
│ subject                  │      │ user_id (FK) ────────────│──► users
│ body_html                │      │ event_type               │
│ variables                │      │ subject                  │
│ is_active                │      │ body_html                │
└──────────────────────────┘      │ recipient_email          │
                                  │ status                   │
┌──────────────────────────┐      │ error_message            │
│   token_blocklist        │      │ sent_at                  │
├──────────────────────────┤      └──────────────────────────┘
│ id (PK)                  │
│ jti (UNIQUE, INDEX)      │
│ token_type               │
│ user_id (FK) ────────────│──► users
└──────────────────────────┘
```

---

## 16. Flujos de Negocio

### 16.1 Registro de Usuario

```
[Android: RegisterActivity]
    │
    ├── POST /api/v1/auth/register
    │   Body: { email, password, full_name, id_number, phone?, address? }
    │
    ▼
[Backend: auth.py → AuthService.register()]
    │
    ├── Valida email unico
    ├── Valida id_number unico
    ├── Crea User con rol="owner"
    ├── Hash de contrasena con bcrypt
    │
    ├── NotificationService.send_notification(user, "user_registered", {...})
    │   └── Envia email de bienvenida (async)
    │
    └── Respuesta: { success: true, data: { user } }
         │
         ▼
[Android: auto-login → guarda sesion → MainActivity]
```

### 16.2 Creacion de Reserva

```
[Android: CrearReservaActivity]
    │
    ├── 1. Carga paralela:
    │   ├── GET /api/v1/pets/        → Lista mascotas del usuario
    │   ├── GET /api/v1/rooms        → Lista habitaciones disponibles
    │   └── GET /api/v1/services     → Lista servicios adicionales
    │
    ├── 2. Usuario selecciona mascota, habitacion, fechas, servicios
    │
    ├── 3. Calculo de precio local (preview)
    │
    ├── 4. POST /api/v1/reservations/
    │   Body: { pet_id, room_id, check_in_date, check_out_date,
    │           lodging_type, notes?, service_ids[] }
    │
    ▼
[Backend: reservations.py → ReservationService.create_reservation()]
    │
    ├── Valida: fecha no en pasado
    ├── Valida: mascota pertenece al owner y no eliminada
    ├── Valida: habitacion existe y activa
    ├── Valida: disponibilidad (no hay solapamiento)
    ├── Valida: servicios solo para "special", sin duplicados
    │
    ├── Calculo servidor:
    │   total = room.price_per_night * num_noches
    │   + sum(service.price * num_noches)
    │
    ├── Crea: Reservation + ReservationService por cada servicio
    │
    ├── NotificationService.send_notification(user, "reservation_confirmed", {...})
    │   └── Email de confirmacion (async)
    │
    └── Respuesta: { success: true, data: { reservation con servicios } }
```

### 16.3 Ciclo de Vida de una Reserva

```
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  1. CREACION (owner)                                   │
  │     POST /reservations/                                │
  │     → status: "confirmed"                              │
  │     → Notificacion: reservation_confirmed              │
  │                                                        │
  │  2. MODIFICACION (owner, solo si confirmed)            │
  │     PUT /reservations/<id>                             │
  │     → Puede cambiar: fechas, habitacion, servicios     │
  │     → Re-verifica disponibilidad                       │
  │     → Recalcula precio                                 │
  │     → Notificacion: reservation_modified               │
  │                                                        │
  │  3. CHECK-IN (admin)                                   │
  │     PATCH /reservations/<id>/status                    │
  │     → status: "confirmed" → "in_progress"              │
  │     → Notificacion: lodging_started                    │
  │                                                        │
  │  4. CHECK-OUT (admin)                                  │
  │     PATCH /reservations/<id>/status                    │
  │     → status: "in_progress" → "completed"              │
  │     → Notificacion: lodging_ended                      │
  │                                                        │
  │  5. CANCELACION (owner o admin, si no completada)      │
  │     DELETE /reservations/<id>  (owner)                 │
  │     PATCH /reservations/<id>/status  (admin)           │
  │     → status: → "cancelled"                            │
  │     → Notificacion: reservation_cancelled              │
  │                                                        │
  └────────────────────────────────────────────────────────┘
```

### 16.4 Formula de Calculo de Precios

```
num_noches = (check_out_date - check_in_date).days

precio_habitacion = room.price_per_night * num_noches

precio_servicios = sum(
    service.price * num_noches
    for service in servicios_seleccionados
)

TOTAL = precio_habitacion + precio_servicios
```

**Ejemplo:**
- Habitacion S-201 (Suite Premium): CRC 30,000/noche
- Servicios: Bano completo (CRC 8,000) + Paseo diario (CRC 5,000)
- Estadia: 3 noches
- **Total**: (30,000 x 3) + (8,000 x 3) + (5,000 x 3) = 90,000 + 24,000 + 15,000 = **CRC 129,000**

---

## 17. Despliegue con Docker

### docker-compose.yml

El sistema se despliega con dos servicios:

**Servicio `db` (PostgreSQL):**
- Imagen: `postgres:16-alpine`
- Puerto: 5432
- Credenciales: `petlodge` / `petlodge`
- Volumen persistente: `pgdata`

**Servicio `api` (Flask):**
- Puerto: 5000
- Depende de: `db`
- Volumen: monta el directorio local (hot-reload)
- Comando de inicio: `flask db upgrade && flask seed && python run.py`
  1. Ejecuta migraciones pendientes
  2. Carga datos iniciales (habitaciones, admin, demo, plantillas)
  3. Inicia el servidor Flask

### Variables de Entorno

| Variable | Valor (desarrollo) |
|----------|-------------------|
| `FLASK_ENV` | `development` |
| `DATABASE_URL` | `postgresql://petlodge:petlodge@db:5432/petlodge` |
| `SECRET_KEY` | `dev-secret-key-change-in-prod` |
| `JWT_SECRET_KEY` | `dev-jwt-secret-change-in-prod` |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USE_TLS` | `true` |
| `MAIL_USERNAME` | `petlodge91@gmail.com` |
| `MAIL_DEFAULT_SENDER` | `noreply@petlodge.com` |
| `ADMIN_EMAIL` | `admin@petlodge.com` |
| `ADMIN_PASSWORD` | `Admin123!` |

### Comandos Utiles

```bash
# Levantar todo el sistema
docker-compose up --build

# Solo la base de datos
docker-compose up db

# Ejecutar seeds manualmente
docker-compose exec api flask seed

# Ejecutar migraciones
docker-compose exec api flask db upgrade

# Crear nueva migracion
docker-compose exec api flask db migrate -m "descripcion"
```

---

## 18. Decisiones de Diseno

### 18.1 Soft Delete de Mascotas
Las mascotas no se eliminan fisicamente de la base de datos. Se usa un campo `is_deleted=True` para mantener la integridad referencial con reservas historicas.

### 18.2 Envio Asincrono de Emails
El `NotificationService` usa `threading.Thread` para enviar emails sin bloquear la respuesta HTTP al cliente. El registro de notificacion se crea primero con `status=pending`, y el hilo actualiza a `sent` o `failed`.

### 18.3 Calculo de Precios en el Servidor
El precio total siempre se calcula en el backend a partir del precio de la habitacion y servicios. Nunca se confia en el precio enviado por el cliente. El precio mostrado en la app Android es solo un preview.

### 18.4 Verificacion de Disponibilidad con Exclusion
Al modificar una reserva, la verificacion de disponibilidad excluye la reserva actual (`exclude_reservation_id`) para evitar falsos conflictos consigo misma.

### 18.5 Servicios Solo para Hospedaje Especial
Los servicios adicionales solo se permiten cuando `lodging_type == "special"`. Esta regla se valida a nivel de la capa de servicios (backend), no solo en la UI.

### 18.6 Fotos en Base64
La app Android convierte la foto de la mascota a base64 y la envia en el JSON del request. El backend la decodifica y la guarda como archivo JPEG con un nombre UUID en `/static/uploads/`. Este enfoque simplifica la implementacion al evitar multipart uploads.

### 18.7 Maquina de Estados para Reservas
Las transiciones de estado de las reservas estan definidas explicitamente en un diccionario `VALID_TRANSITIONS`. Esto previene transiciones invalidas (ej: no se puede reactivar una reserva completada o cancelada).

### 18.8 Networking del Android App
La IP del servidor backend se configura en `ApiClient.SERVER_IP`. Para el emulador Android se usa `10.0.2.2` (alias estandar de localhost del host). Para dispositivos fisicos en la red local se configura la IP LAN del servidor (actualmente `192.168.50.232`).

### 18.9 Patron de Respuesta Estandarizado
Todas las respuestas de la API siguen el mismo formato:
- Exito: `{ success: true, message: "...", data: {...} }`
- Error: `{ success: false, error: "...", code: "ERROR_CODE" }`

Esto simplifica el manejo de respuestas en la app Android con un unico `ApiResponse<T>` generico.

### 18.10 Comandos CLI para Seeds
Los datos iniciales se cargan mediante comandos CLI de Flask (`flask seed`), lo que permite ejecutarlos tanto en desarrollo como en el pipeline de Docker de forma consistente.
