# DRF Clean Architecture Notes API

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

## Architecture

The project follows a layered structure inspired by clean architecture principles.
notes_commented/
│
├── models.py
├── domain/
│ └── note_and_comments_result.py
│
├── repositories/
│ ├── note_repository.py
│ └── comment_repository.py
│
├── commands/
│ ├── note_delete.py
│ ├── note_restore.py
│ ├── comment_delete.py
│ └── comment_restore.py
│
└── api/
├── serializers.py
├── views.py
└── urls.py


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
POST /api/notess/
GET /api/notess/
GET /api/notess/{id}/
PUT /api/notess/{id}/
DELETE /api/notess/{id}/
POST /api/notess/{id}/restore/

### Comments
GET /api/notess/{note_id}/comments/
POST /api/notess/{note_id}/comments/
PUT /api/comments/{id}/
DELETE /api/comments/{id}/
POST /api/comments/{id}/restore/

---

## Business Rules

- Notes and comments support **soft delete**.
- Deleted notes cannot receive new comments.
- Deleting a note **soft deletes its related comments**.
- Comments cannot be modified if their parent note is deleted.
- Restore operations re-enable previously deleted records.

---

## How to Run

### 1. Clone repository
git clone https://github.com/Felipee-M/drf-clean-architecture-notes.git

cd drf-clean-architecture-notes

### 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
python manage.py migrate

### 5. Start server
python manage.py runserver

---

## Example Requests (HTTPie)

Create note
http POST :8000/api/notess/ title="First note" content="Example content"

Create comment
http POST :8000/api/notess/1/comments/ text="First comment"

Delete note
http DELETE :8000/api/notess/1/

Restore note
http POST :8000/api/notess/1/restore/

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