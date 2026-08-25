# Coderr

[🇬🇧 English version](README.MD)

## Beschreibung

Dieses Projekt wurde als Lernprojekt entwickelt, um die Entwicklung einer Webanwendung mit Django und dem Django REST Framework praxisnah zu erlernen. Im Fokus steht die Umsetzung eines Backends mit einer REST API, über die ein bereitgestelltes Frontend mit dem Backend kommuniziert. Dabei werden unter anderem HTTP-Anfragen verarbeitet und geschützte Endpunkte tokenbasiert abgesichert.

Darüber hinaus bietet die API Funktionen zur Filterung, Suche und Sortierung von Daten. Zusätzlich werden Pagination-Mechanismen eingesetzt, um größere Datenmengen übersichtlich und effizient über die API bereitzustellen.

---

# Features

* REST API auf Basis von Django REST Framework
* Verwendung von Django REST Framework Views (`generics` und `APIView`)
* Token-basierte Authentifizierung
* Modulare Struktur durch eigene Django-Apps
* Erweiterbare API-Struktur über URL-Routing

---

# Technologien

| Technologie           | Version             |
| --------------------- | ------------------- |
| Python                | 3.13.3              |
| Django                | 6.0.7               |
| Django REST Framework | 3.17.1              |
| Django Cors Headers   | 4.9.0               |
| Django Filter         | 26.1                |
| Pillow                | 12.3.0              |
| Factory Boy           | 3.3.3               |
| Datenbank             | SQLite3             |
| Authentifizierung     | TokenAuthentication |

---

# Voraussetzungen

Folgende Software wird benötigt:

* Python 3.13.3 oder höher
* pip
* Git

Das Projekt wurde unter Windows entwickelt.

Da es sich um eine Django Web API handelt, sollte die Anwendung grundsätzlich auch unter anderen Betriebssystemen mit Python-Unterstützung lauffähig sein.

Mögliche Betriebssysteme:

* Windows
* Linux
* macOS

---

# Installation

## 1. Repository herunterladen

Repository klonen:

```bash
git clone [REPOSITORY_URL]
```

In das Projektverzeichnis wechseln:

```bash
cd [PROJECT_DIRECTORY]
```

---

## 2. Virtuelle Umgebung erstellen

Es wird empfohlen, eine virtuelle Python-Umgebung zu verwenden.

Erstellen:

```bash
python -m venv venv
```

Aktivieren unter Windows:

```bash
venv\Scripts\activate
```

Aktivieren unter Linux/macOS:

```bash
source venv/bin/activate
```

---

## Sample Data

Die Datenbank kann mit Beispieldaten über folgenden Befehl befüllt werden:

```bash
python manage.py shell -c "from factories import create_all; create_all()"
```

---

## 3. Abhängigkeiten installieren

Die benötigten Python-Pakete installieren:

```bash
pip install -r requirements.txt
```

---

# Projektkonfiguration

## Umgebungsvariablen

Aktuell werden keine zusätzlichen Umgebungsvariablen benötigt.

Die vorhandene `.env` Datei ist derzeit leer und enthält keine projektrelevanten Einstellungen.

---

# Django Apps

Das Projekt verwendet folgende Django Apps:

| App             | Beschreibung                                                                                          |
| ------------    | ----------------------------------------------------------------------------------------------------- |
| `auth_app`      | Stellt API-Endpunkte für Benutzerregistrierung, Anmeldung und tokenbasierte Authentifizierung bereit. |
| `freelance_app` | Stellt API-Endpunkte für Profile, Offer, OfferDetail, Order und Review bereit.                        |

Zusätzlich werden folgende Django-Komponenten verwendet:

* `rest_framework`
* `rest_framework.authtoken`
* `django_filters`

---

# Datenbank

Das Projekt verwendet die von Django standardmäßig unterstützte SQLite-Datenbank.

SQLite wird verwendet, da das Projekt als Lernprojekt entwickelt wird und aktuell keine Anforderungen an eine externe oder produktionsorientierte Datenbank bestehen.

Die Datenbank wird lokal über folgende Datei verwaltet:

db.sqlite3

---

# Migrationen

Migrationen verwalten Änderungen an der Datenbankstruktur.

Aktueller Stand:

* Es existieren aktuell keine eigenen Datenbankmigrationen.

Sobald Django Models erstellt oder verändert werden, müssen Migrationen erzeugt werden.

Neue Migration erstellen:

```bash
python manage.py makemigrations
```

Migrationen anwenden:

```bash
python manage.py migrate
```

---

# Superuser erstellen

Für den Zugriff auf das Django Admin Interface kann ein Administrator erstellt werden:

```bash
python manage.py createsuperuser
```

Danach ist der Admin-Bereich erreichbar unter:

```
admin/
```

---

# Entwicklungsserver starten

Der lokale Entwicklungsserver wird gestartet mit:

```bash
python manage.py runserver
```

Standardmäßig ist die Anwendung erreichbar unter:

```
http://127.0.0.1:8000/
```

---

# Authentifizierung

Die API verwendet eine Token-basierte Authentifizierung.

Verwendetes Django REST Framework Modul:

```
rest_framework.authtoken
```

Authentifizierung:

```
rest_framework.authentication.TokenAuthentication
```

Geschützte API-Anfragen müssen einen gültigen Token im Header senden.

Beispiel:

```http
Authorization: Token [USER_TOKEN]
```

---

# API Endpunkte

Die Anwendung stellt folgende API-Endpunkte bereit:

| Nr. | Methode  | Endpunkt                                          | Name                           | Beschreibung                                                                                 |
| --- | -------- | ------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| 1   | POST     | `api/registration/`                               | registration                   | User registrieren, zusätzlich wird auch ein Profil erstellt                                  |
| 2   | POST     | `api/login/`                                      | login                          | User einloggen                                                                               |
| 3   | GET      | `api/profile/<pk>/`                               | profile-detail                 | Gibt die Daten eines einzelnen Profil zurück                                                 |
| 4   | PATCH    | `api/profile/<pk>/`                               | profile-detail                 | Aktualisiert einen bestehenden Profil                                                        |
| 5   | GET      | `api/api/profiles/business/`                      | profiles-business-list         | Ruft alle Profile ab, die als Typ (`business`) eingetragen haben                             |
| 6   | GET      | `api/api/profiles/customer/`                      | profiles-customer-list         | Ruft alle Profile ab, die als Typ (`customer`) eingetragen haben                             |
| 7   | GET      | `api/offers/`                                     | offer-list                     | Ruft alle Angebote ab                                                                        |
| 8   | POST     | `api/offers/`                                     | offer-list                     | Erstellt ein neues Angebot und deren drei Angebot-Details                                    |
| 9   | GET      | `api/offers/<id>/`                                | offer-detail                   | Gibt die Daten eines einzelnen Angebots zurück und deren drei Angebot-Details                |
| 10  | PATCH    | `api/offers/<id>/`                                | offer-detail                   | Aktualisiert ein bestehendes Angebot und deren drei Angebot-Details                          |
| 11  | DELETE   | `api/offers/<id>/`                                | offer-detail                   | Löscht ein bestehendes Angebot und deren drei Angebot-Details                                |
| 12  | GET      | `api/offerdetails/<id>/`                          | offerdetails-detail            | Gibt die Daten von einem einzelnen Angebot-Detail zurück                                     |
| 13  | GET      | `api/orders/`                                     | order-list                     | Ruft alle Bestellungen ab                                                                    |
| 14  | POST     | `api/orders/`                                     | order-list                     | Erstellt eine neue Bestellung                                                                |
| 15  | PATCH    | `api/orders/<id>/`                                | order-detail                   | Aktualisiert eine bestehende Bestellung                                                      |
| 16  | DELETE   | `api/orders/<id>/`                                | order-detail                   | Löscht eine bestehende Bestellung                                                            |
| 17  | GET      | `api/order-count/<business_user_id>/`             | order-count-detail             | Gibt die Anzahl an laufenden Bestellungen eines Profil des Types (`business`) zurück         |
| 18  | GET      | `api/completed-order-count/<business_user_id>/`   | completed-order-count-detail   | Gibt die Anzahl an abgeschlossenen Bestellungen eines Profil des Types (`business`) zurück   |
| 19  | GET      | `api/reviews/`                                    | review-list                    | Ruft alle Rezensionen ab                                                                     |
| 20  | POST     | `api/reviews/`                                    | review-list                    | Erstellt eine neue Rezension                                                                 |
| 21  | PATCH    | `api/reviews/<id>/`                               | review-detail                  | Aktualisiert eine bestehende Rezension                                                       |
| 22  | DELETE   | `api/reviews/<id>/`                               | review-detail                  | Löscht eine bestehende Rezension                                                             |
| 23  | GET      | `api/base-info/`                                  | base-info-list                 | Ruft allgemeine Basisinformationen ab, <br>wie Anzahl der Bewertungen, Anzahl der Geschäftsnutzer und Anzahl der Angebote, <br>außerdem das durchschnittliche Bewertungsergebnis.                                                                                                                                     |

---

# Projektstruktur

```
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

Das Projekt enthält automatisierte Tests.

Alle Tests ausführen:

```bash
python manage.py test
```

Nur die Tests einer bestimmten Testdatei ausführen:

```bash
python manage.py test auth_app.tests
python manage.py test freelance_app.tests.test_base_info
python manage.py test freelance_app.tests.test_offer
python manage.py test freelance_app.tests.test_order
python manage.py test freelance_app.tests.test_profile
python manage.py test freelance_app.tests.test_review
```

---

# Django Management Commands

Es wurden keine eigenen Django Management Commands implementiert.

---

# Deployment

Aktuell ist kein produktives Deployment eingerichtet.

Das Projekt befindet sich derzeit in einer lokalen Entwicklungsumgebung.

---

# Sicherheitshinweise

Das Projekt befindet sich aktuell in einer Entwicklungsumgebung und dient zu Lern- und Demonstrationszwecken.

Bei einer Weiterentwicklung zu einer öffentlich betriebenen Anwendung müssten unter anderem folgende Punkte berücksichtigt werden:

* sichere Verwaltung des `SECRET_KEY`
* Konfiguration von `ALLOWED_HOSTS`
* Aktivierung von HTTPS
* Überprüfung der Datenbankwahl
* sichere Verwaltung von Authentifizierungs-Tokens

---

# Technische Besonderheiten

* Verwendung von `django-filter` zur Filterung von Querysets
* Verwendung von `Pillow` zur Verarbeitung von Bildern
* Verwendung von `factory_boy` zur Erstellung von Testdaten
* SQLite wird für die lokale Entwicklung verwendet

---

# Lizenz

© 2026 Leonard Fritzmann

Alle Rechte vorbehalten.

Dieses Projekt dient ausschließlich Lern- und Portfoliozwecken. Eine Nutzung, Vervielfältigung oder Weitergabe des Quellcodes ist ohne ausdrückliche Genehmigung nicht gestattet.

---

# Kontakt

Bei Fragen oder Anmerkungen:

* E-Mail: contact@leonard-fritzmann.de