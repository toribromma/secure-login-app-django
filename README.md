# Secure Login App (Django)

Server-rendered Django auth demo with secure defaults: cookie sessions, CSRF, rate limiting/lockout (django-axes), and Argon2 password hashing.

## Setup
1) Create & activate venv (Windows):
```
python -m venv .venv
.venv\Scripts\activate
```
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Run migrations:
```
python manage.py migrate
```
4) Start server:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/

## Auth Flow
- Register: `/register`
- Login: `/login` (sets HttpOnly session cookie; guarded by django-axes lockouts)
- Me (protected): `/me` (`@login_required`)
- Logout: `/logout`

## Security Settings (key ones in `securelogin/settings.py`)
- Session/CSRF cookies: set to Secure + SameSite Lax (configure for HTTPS in prod).
- Argon2 hashing (enable in `PASSWORD_HASHERS`).
- Rate-limit/lockout via django-axes (`AUTHENTICATION_BACKENDS` + middleware).
- CSRF protection and built-in Django auth/session middleware.

## Tests
Run all tests (with venv active):
```
python manage.py test accounts
```

## Admin (optional)
Create a superuser to access `/admin/`:
```
python manage.py createsuperuser
```
