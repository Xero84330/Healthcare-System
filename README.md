# Healthcare Backend

A Django REST Framework backend for a healthcare application. It provides user registration and login, patient and doctor record management, and patient-doctor assignment, all secured with JWT authentication and backed by PostgreSQL.

## Stack

| Component | Choice |
|---|---|
| Framework | Django 6.1 + Django REST Framework |
| Database | PostgreSQL |
| Auth | djangorestframework-simplejwt, with token blacklisting enabled |
| Config | python-dotenv for environment variables |

## Project Structure

The project is organized by layer rather than by Django's default per-app convention. Each app under `Apps/` holds only its model. Serializers, views, and URL configuration are centralized in their own top-level packages.

```
Conf/                    Project settings, root URL configuration, WSGI/ASGI entrypoints
Apps/
    Authentication/       Custom User model (email-based login, no username field)
    Patient/              Patient model
    Doctors/              Doctor model
    Mapping/              Mapping model (patient-doctor assignment)
Serializers/              All DRF serializers
Services/                 All views
Urls/                     All URL modules, included from Conf/urls.py
Tests/                    Automated test suite
manage.py
requirements.txt
```

This layout groups files by responsibility (all models, all serializers, all views, all routes) instead of by feature. Given the small number of resources in this project, it keeps related code adjacent without navigating four separate app directories for each type of file.

### Models

| Model | Fields | Notes |
|---|---|---|
| `User` | `name`, `email`, `password` | `email` is the `USERNAME_FIELD`; there is no separate `username` field. |
| `Patient` | `name`, `created_by`, `created_at`, `updated_at` | `created_by` is a foreign key to `User`. |
| `Doctor` | `name`, `created_by`, `created_at`, `updated_at` | `created_by` is a foreign key to `User`. |
| `Mapping` | `doctor`, `patient`, `created_by`, `created_at`, `updated_at` | `(doctor, patient)` is enforced unique at the database level. |

## Configuration

The application reads its configuration from environment variables, loaded from a `.env` file at the project root (excluded from version control).

```
SECRET_KEY=
DEBUG=True
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

`DEBUG` evaluates to `True` only when the value is the literal string `True`. Any other value, including an unset variable, is treated as `False`.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# populate .env as shown above

python manage.py migrate
python manage.py runserver
```

## Authentication

1. `POST /api/auth/register/` creates an account.
2. `POST /api/auth/login/` returns an access token and a refresh token.
3. Protected endpoints require the access token on every request:

```
Authorization: Bearer <access_token>
```

Access tokens are valid for 30 minutes, refresh tokens for 7 days.

Login blacklists all previously issued refresh tokens for that user. Each successful login invalidates every refresh token issued in prior sessions for the same account; only the most recent login's refresh token remains usable. Access tokens already issued are unaffected and remain valid until they expire on their own, since access tokens are not blacklisted.

## API Reference

### Authentication

| Method | Endpoint | Auth | Request Body |
|---|---|---|---|
| POST | `/api/auth/register/` | No | `name`, `email`, `password` |
| POST | `/api/auth/login/` | No | `email`, `password` |

Registration runs Django's configured password validators and enforces email uniqueness at the serializer level.

### Patients

| Method | Endpoint | Auth | Scope |
|---|---|---|---|
| POST | `/api/patients/` | Required | Creates a patient owned by the requesting user. |
| GET | `/api/patients/` | Required | Returns patients created by the requesting user only. |
| GET | `/api/patients/<id>/` | Required | Requesting user's own patients only. |
| PUT | `/api/patients/<id>/` | Required | Requesting user's own patients only. |
| DELETE | `/api/patients/<id>/` | Required | Requesting user's own patients only. |

A request for a patient ID that exists but belongs to a different user returns `404`, not `403`. This follows the assignment specification directly: patient listing is defined as scoped to the authenticated user, and that scope is applied consistently across all patient endpoints.

### Doctors

| Method | Endpoint | Auth | Scope |
|---|---|---|---|
| POST | `/api/doctors/` | Required | Creates a doctor record. |
| GET | `/api/doctors/` | Required | Returns all doctors, unscoped. |
| GET | `/api/doctors/<id>/` | Required | Any doctor record. |
| PUT | `/api/doctors/<id>/` | Required | Any doctor record. |
| DELETE | `/api/doctors/<id>/` | Required | Any doctor record. |

Doctor endpoints are not scoped to the creating user. The specification defines doctor retrieval as "all doctors" with no ownership qualifier, and that is what is implemented: any authenticated user can read, update, or delete any doctor record, regardless of who created it.

### Patient-Doctor Mappings

| Method | Endpoint | Auth | Scope |
|---|---|---|---|
| POST | `/api/mappings/` | Required | Creates a mapping from `patient` and `doctor` IDs. |
| GET | `/api/mappings/` | Required | Returns all mappings, unscoped. |
| GET | `/api/mappings/<patient_id>/` | Required | Returns all mappings for the given patient ID. |
| DELETE | `/api/mappings/<id>/` | Required | Deletes the mapping with the given mapping ID. |

The `GET` and `DELETE` routes on `/api/mappings/<id>/` share a URL pattern but resolve `id` against different fields: `GET` treats it as a patient ID, `DELETE` treats it as the mapping's own primary key. This is a direct implementation of the specification, which defines these two operations with different identifier semantics under the same path shape. Callers should not assume the ID passed to one method is interchangeable with the other.

Creating a mapping does not verify that the referenced patient belongs to the requesting user. Any authenticated user can assign a doctor to any patient ID that exists in the system, including patients created by other users. Mapping retrieval and deletion are likewise unscoped by creator. The specification defines these endpoints without an ownership qualifier, matching how doctor endpoints are also left unscoped.

## Access Control Summary

| Resource | Read scope | Write/Delete scope |
|---|---|---|
| Patients | Creator only | Creator only |
| Doctors | All users | All users |
| Mappings | All users | All users |

Patients are the only resource scoped to the creating user, because the specification explicitly defines patient retrieval that way. Doctors and mappings are implemented as shared resources, consistent with how the specification defines their retrieval and without an added restriction the specification does not call for.

## Testing

The `Tests/` package contains the automated test suite, run with:

```bash
python manage.py test Tests
```

| File | Coverage |
|---|---|
| `test_auth.py` | Registration followed by login returns both tokens; login with an incorrect password is rejected. |
| `test_patients.py` | An owner can retrieve their own patient; a different authenticated user is denied access to that patient (404); an unauthenticated request is rejected (401). |
| `test_mapping.py` | A mapping is created successfully; a duplicate `(doctor, patient)` pair is rejected by the unique constraint. |

Endpoints not covered by the automated suite have been verified manually against a running instance, including foreign key validation on mapping creation and duplicate email rejection on registration.