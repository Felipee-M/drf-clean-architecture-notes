# DRF Notes API – Clean Architecture Study Project
![Python](https://img.shields.io/badge/python-3.x-blue)
![Django](https://img.shields.io/badge/django-REST%20Framework-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Study project built with **Django REST Framework** to practice a layered architecture using **Repository and Command patterns**.

The API manages **notes and comments**, supporting soft delete, restore operations and nested resources.

---

## Features

- Notes CRUD
- Comments nested under notes
- Soft delete for notes and comments
- Restore endpoints
- Cascade soft delete (deleting a note also soft deletes its comments)
- Repository pattern
- Command layer for business actions
- Domain result enums for command outcomes

---

## Project Structure

```text
drf-clean-architecture-notes
│
├── config/                  # Django project configuration
│   ├── settings.py
│   └── urls.py
│
├── notes_commented/         # Main application
│   ├── models.py            # Database models
│   ├── domain/              # Domain result enums
│   ├── repositories/        # Data access layer
│   ├── commands/            # Business actions
│   └── api/                 # API layer (views, serializers, urls)
│
├── manage.py
├── requirements.txt
└── README.md
```

## Architecture
```text
The project follows a layered structure inspired by clean architecture principles.
notes_commented/
│
├── models.py
├── domain/
│   └── note_and_comments_result.py
├── repositories/
│   ├── note_repository.py
│   └── comment_repository.py
├── commands/
│   ├── note_delete.py
│   ├── note_restore.py
│   ├── comment_delete.py
│   └── comment_restore.py
└── api/
    ├── serializers.py
    ├── views.py
    └── urls.py
```

```text
Request
   │
   ▼
ViewSet (API Layer)
   │
   ▼
Commands (Business Actions)
   │
   ▼
Repositories (Data Access)
   │
   ▼
Django ORM / Database
```

### Responsibilities

**Models**
- Define database structure.

**Repositories**
- Encapsulate database access.

**Commands**
- Implement business actions and rules.

**Domain**
- Define result enums used by commands.

**API**
- Expose endpoints via Django REST Framework.

---

## Main Endpoints

### Notes
```http
POST /api/notess/
GET /api/notess/
GET /api/notess/{id}/
PUT /api/notess/{id}/
DELETE /api/notess/{id}/
POST /api/notess/{id}/restore/
```

### Comments
```http
GET /api/notess/{note_id}/comments/
POST /api/notess/{note_id}/comments/
PUT /api/comments/{id}/
DELETE /api/comments/{id}/
POST /api/comments/{id}/restore/
```
---

## Example Response

GET /api/notess/

```json
[
  {
    "id": 1,
    "title": "First note",
    "content": "Example content",
    "deleted": false,
    "created_at": "2026-03-10T10:00:00Z",
    "updated_at": "2026-03-10T10:00:00Z"
  }
]
```

## Business Rules

- Notes and comments support **soft delete**.
- Deleted notes cannot receive new comments.
- Deleting a note **soft deletes its related comments**.
- Comments cannot be modified if their parent note is deleted.
- Restore operations re-enable previously deleted records.

---

## How to Run

### 1. Clone repository
```http
git clone https://github.com/Felipee-M/drf-clean-architecture-notes.git

cd drf-clean-architecture-notes
```
### 2. Create virtual environment
```http
python -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies
```http
pip install -r requirements.txt
```
### 4. Run migrations
```http
python manage.py migrate
```
### 5. Start server
```http
python manage.py runserver
```
---
## Example Requests (HTTPie)

Create note
```http
http POST :8000/api/notess/ title="First note" content="Example content"
```
Create comment
```http
http POST :8000/api/notess/1/comments/ text="First comment"
```
Delete note
```http
http DELETE :8000/api/notess/1/
```
Restore note
```http
http POST :8000/api/notess/1/restore/
```
---

## Tech Stack

- Python
- Django
- Django REST Framework
- HTTPie (for testing)

---

## Purpose

This project was created as part of a backend learning path to practice:

- REST API design
- Django ORM
- Layered architecture
- Business rule isolation
- Clean code structure

## What I Practiced

This project was created to practice backend development concepts such as:

- Django REST Framework API design
- Repository pattern
- Command pattern
- Soft delete strategies
- Nested resources
- Separation of business logic from API layer