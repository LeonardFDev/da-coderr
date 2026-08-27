# Coderr

[🇩🇪 Deutsche Version](README_DE.MD)

## Description

This project was developed as a learning project to provide hands-on experience in developing a web application using Django and the Django REST Framework. The focus is on implementing a backend with a REST API through which a provided frontend communicates with the backend. Among other things, HTTP requests are processed, and protected endpoints are secured using token-based authentication.

Furthermore, the API offers functions for filtering, searching, and sorting data. Pagination mechanisms are also used to provide large amounts of data clearly and efficiently via the API.

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/LeonardFDev/da-coderr.git .
```

### 2. Create and activate a virtual environment

#### Create: 
```bash
python -m venv env
```
#### Activate:

Windows CMD:

```bash
"env/Scripts/activate" 
```

Windows PowerShell:

```bash
.\env\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source ./env/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

---

# Features

* REST API based on Django REST Framework
* Use of Django REST Framework Views (`generics` and `APIView`)
* Token-based authentication
* Modular structure through custom Django apps
* Extensible API structure through URL routing

---

# Technologies

| Technology            | Version             |
| --------------------- | ------------------- |
| Python                | 3.13.3              |
| Django                | 6.0.6               |
| Django REST Framework | 3.17.1              |
| Django Cors Headers   | 4.9.0               |
| Django Filter         | 26.1                |
| Pillow                | 12.3.0              |
| Factory Boy           | 3.3.3               |
| Database              | SQLite3             |
| Authentication        | TokenAuthentication |

---

# Requirements

The following software is required:

* Python 3.13.3 or later
* pip
* Git

The project was developed on Windows.

Since this is a Django Web API, the application should generally run on other operating systems that support Python.

Supported operating systems include:

* Windows
* Linux
* macOS

---

# Installation

## 1. Clone the repository

Clone the repository:

```bash
git clone [REPOSITORY_URL]
```

Navigate to the project directory:

```bash
cd da-coderr
```

---

## 2. Create a virtual environment

It is recommended to use a Python virtual environment.

Create the virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

---

## Sample Data

You can populate the database with sample data using the following command:

```bash
python manage.py shell -c "from factories import create_all; create_all()"
```

---

## 3. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# Django Apps

The project uses the following Django apps:

| App             | Description                                                                          |
| --------------- | ------------------------------------------------------------------------------------ |
| `auth_app`      | Provides API endpoints for user registration, login, and token-based authentication. |
| `freelance_app` | Provides API endpoints for Profile, Offer, OfferDetail, Order and Review.            |

Additionally, the following Django components are used:

* `rest_framework`
* `rest_framework.authtoken`
* `django_filters`

---

# Database

The project uses Django's default SQLite database.

SQLite is used because this project is intended as a learning project and currently has no requirements for an external or production-oriented database.

The database is managed locally through the following file:

```text
db.sqlite3
```

---

# Migrations

Migrations manage changes to the database schema.

Current status:

* No custom database migrations currently exist.

Whenever Django models are created or modified, new migrations must be generated.

Create new migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

# Create a Superuser

To access the Django Admin interface, create an administrator account:

```bash
python manage.py createsuperuser
```

The admin interface will then be available at:

```text
admin/
```

---

# Start the Development Server

Start the local development server with:

```bash
python manage.py runserver
```

By default, the application is available at:

```text
http://127.0.0.1:8000/
```

---

# Authentication

The API uses token-based authentication.

Django REST Framework module used:

```text
rest_framework.authtoken
```

Authentication method:

```text
rest_framework.authentication.TokenAuthentication
```

Protected API requests must include a valid authentication token in the request header.

Example:

```http
Authorization: Token [USER_TOKEN]
```

---

# API Endpoints

The application provides the following API endpoints:

| No. | Method   | Endpoint                                          | Name                           | Description                                                                                  |
| --- | -------- | ------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| 1   | POST     | `api/registration/`                               | registration                   | Register User, in addition, a profile is also created                                        |
| 2   | POST     | `api/login/`                                      | login                          | Log in user                                                                                  |
| 3   | GET      | `api/profile/<pk>/`                               | profile-detail                 | Retrieves the data of a single profile                                                       |
| 4   | PATCH    | `api/profile/<pk>/`                               | profile-detail                 | Updates an existing profile                                                                  |
| 5   | GET      | `api/api/profiles/business/`                      | profiles-business-list         | Retrieve all profiles that have entered (`business`) as their type                           |
| 6   | GET      | `api/api/profiles/customer/`                      | profiles-customer-list         | Retrieve all profiles that have entered (`customer`) as their type                           |
| 7   | GET      | `api/offers/`                                     | offer-list                     | Retrieve all offers                                                                          |
| 8   | POST     | `api/offers/`                                     | offer-list                     | Create a new offer and its three offer details                                               |
| 9   | GET      | `api/offers/<id>/`                                | offer-detail                   | Retrieves the data for a single offer and its three offer details                            |
| 10  | PATCH    | `api/offers/<id>/`                                | offer-detail                   | Updates an existing offer and its three offer details                                        |
| 11  | DELETE   | `api/offers/<id>/`                                | offer-detail                   | Deletes an existing offer and its three offer details                                        |
| 12  | GET      | `api/offerdetails/<id>/`                          | offerdetails-detail            | Retrieves the data for a single offer detail                                                 |
| 13  | GET      | `api/orders/`                                     | order-list                     | Retrieve all orders                                                                          |
| 14  | POST     | `api/orders/`                                     | order-list                     | Creates a new order                                                                          |
| 15  | PATCH    | `api/orders/<id>/`                                | order-detail                   | Updates an existing order                                                                    |
| 16  | DELETE   | `api/orders/<id>/`                                | order-detail                   | Deletes an existing order                                                                    |
| 17  | GET      | `api/order-count/<business_user_id>/`             | order-count-detail             | Retrieves the number of active orders for a profile of type (`business`)                     |
| 18  | GET      | `api/completed-order-count/<business_user_id>/`   | completed-order-count-detail   | Retrieves the number of completed orders for a profile of type (`business`)                  |
| 19  | GET      | `api/reviews/`                                    | review-list                    | Retrieve all reviews                                                                         |
| 20  | POST     | `api/reviews/`                                    | review-list                    | Creates a new review                                                                         |
| 21  | PATCH    | `api/reviews/<id>/`                               | review-detail                  | Updates an existing review                                                                   |
| 22  | DELETE   | `api/reviews/<id>/`                               | review-detail                  | Deletes an existing review                                                                   |
| 23  | GET      | `api/base-info/`                                  | base-info-list                 | Retrieves general basic information, <br>such as the number of reviews, the number of business profiles, and the number of listings, <br>as well as the average review score.                                                                                                                                                |

---

# Project Structure

```text
Coderr
│
├── .gitignore
├── db.sqlite3
├── factories.py
├── manage.py
├── requirements.txt
│
├── core
│   ├── settings.py
│   └── urls.py
│
├── tests
|    └── helpers.py
│
├── auth_app
│   ├── models.py
|   ├── admin.py
│   ├── tests.py
│   ├── migrations/
|   └── api
|       ├── serializers.py
|       ├── urls.py
|       └── views.py
│
└── freelance_app
    ├── models.py
    ├── admin.py
    ├── migrations/
    ├── api
    |   ├── filters.py
    |   ├── pagination.py
    |   ├── permissions.py
    |   ├── serializers.py
    |   ├── urls.py
    |   └── views.py
    |
    └── tests
        ├── test_base_info.py
        ├── test_offer.py
        ├── test_order.py
        ├── test_profile.py
        ├── test_review.py
        └── datas
            ├── data_offer.py
            ├── data_order.py
            ├── data_profile.py
            └── data_review.py

```

---

# Tests

The project contains automated tests.

Run all tests:

```bash
python manage.py test
```

Run the tests from a specific test file:

```bash
python manage.py test auth_app.tests
```

```bash
python manage.py test freelance_app.tests.test_base_info
```

```bash
python manage.py test freelance_app.tests.test_offer
```

```bash
python manage.py test freelance_app.tests.test_order
```

```bash
python manage.py test freelance_app.tests.test_profile
```

```bash
python manage.py test freelance_app.tests.test_review
```

---

# Technical Highlights

* Use of `django-filter` for filtering querysets
* Use of `Pillow` for image processing
* Use of `factory_boy` for creating test data
* SQLite is used for local development

---

# License

© 2026 Leonard Fritzmann

All rights reserved.

This project is intended solely for learning and portfolio purposes. Use, reproduction, or redistribution of the source code is not permitted without explicit permission.

---

# Contact

For questions or feedback:

* Email: E-Mail: contact@leonard-fritzmann.de