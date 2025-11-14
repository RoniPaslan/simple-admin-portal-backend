# Simple Admin Portal dengan RBAC & User Invitation - Backend (Django)

Backend ini dibuat dengan **Django + Django REST Framework (DRF)** untuk mengelola Orders, Products, dan Users.
Frontend menggunakan Next.js.

---

## 📦 Persyaratan

* Python 3.13.5
* pip / venv
* SQLite3 / PostgreSQL (sesuaikan `settings.py`)
* Next.js + npm (opsional, hanya untuk frontend)

---

## 🔧 Instalasi

1. **Clone repository**

```bash
git clone https://github.com/RoniPaslan/simple-admin-portal-backend.git
cd backend
```

2. **Buat virtual environment & aktifkan**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Konfigurasi `.env`**
   Buat file `.env` berdasarkan `.env.example`:

```bash
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

5. **Migrasi database**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Buat superuser**

```bash
python manage.py createsuperuser
```

7. **Jalankan server development**

```bash
python manage.py runserver
```

Server akan berjalan di:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📞 Struktur Direktori

```text
backend/
├── manage.py              # Entry point Django project
├── requirements.txt       # Dependencies Python
├── .env.example           # Contoh konfigurasi environment
├── .env                   # Konfigurasi environment
├── db.sqlite3             # Database SQLite
├── venv/                  # Virtual environment Python
├── media/                 # Folder upload file/media
├── portal/                # Django project utama
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                 # App untuk user & auth
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── products/              # App untuk produk
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── orders/                # App untuk order
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── invitations/           # App untuk undangan user
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── tokens.py
    └── urls.py
```

---

## 👥 Role User

1. superadmin (opsional)
2. admin
3. manager
4. staff

---

## 📧 Konfigurasi Email

Untuk testing, email menggunakan **Mailtrap** (SMTP):

```bash
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("MAIL_HOST", "sandbox.smtp.mailtrap.io")
EMAIL_PORT = int(os.getenv("MAIL_PORT", 2525))
EMAIL_HOST_USER = os.getenv("MAIL_USERNAME", "xxxxxxxx")  # username Mailtrap
EMAIL_HOST_PASSWORD = os.getenv("MAIL_PASSWORD", "xxxxxxxx")  # password Mailtrap
EMAIL_USE_TLS = os.getenv("MAIL_ENCRYPTION", "tls").lower() == "tls"
DEFAULT_FROM_EMAIL = "no-reply@example.com"
```

---

## ⚡ Catatan

* Jika hanya ingin backend, Next.js & npm opsional.
* Sesuaikan database di `.env` sesuai kebutuhan (SQLite / PostgreSQL).
* Gunakan `.env.example` sebagai panduan untuk konfigurasi environment.
