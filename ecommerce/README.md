# LUMINA — E-Commerce Store

A full-stack e-commerce application built with Django + vanilla JS.

## Stack
- **Backend**: Django 4.x + Django REST Framework
- **Database**: SQLite (dev) — swap to PostgreSQL for production
- **Frontend**: Vanilla HTML/CSS/JS (single-page app, no framework)

## Features
- Product listings with category filters + search
- Product detail pages
- Shopping cart (persisted in localStorage)
- User registration & login (Django sessions)
- Checkout with shipping address
- Order history per user
- Django Admin panel

## Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework django-cors-headers Pillow

# 2. Apply migrations (already done if using the provided db.sqlite3)
python manage.py migrate

# 3. Create superuser (already seeded: admin / admin123)
python manage.py createsuperuser

# 4. Run
python manage.py runserver

# 5. Open http://localhost:8000
```

## Seeded Data
- **Admin**: username=`admin`, password=`admin123`
- 12 products across 4 categories (Electronics, Clothing, Books, Home & Garden)

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/products/ | List all products |
| GET | /api/products/:id/ | Product detail |
| GET | /api/categories/ | List categories |
| POST | /api/auth/register/ | Register user |
| POST | /api/auth/login/ | Login |
| POST | /api/auth/logout/ | Logout |
| GET | /api/auth/me/ | Current user |
| POST | /api/orders/ | Place order |
| GET | /api/orders/my/ | My orders |
| GET/POST | /admin/ | Django admin |

## Project Structure
```
ecommerce/
├── ecommerce/          # Project config
│   ├── settings.py
│   └── urls.py
├── store/              # Products, orders app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── admin.py
├── templates/
│   └── index.html      # Single-page frontend
├── db.sqlite3          # Pre-seeded database
└── manage.py
```
