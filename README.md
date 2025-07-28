# Flask-Math

Flask-Math is a Python web application that provides a dashboard for monitoring application metrics, user management, math operations, and admin features. The project uses Flask and is structured for modularity and scalability.

## Features

- User registration, authentication, and profile management
- Admin dashboard with application metrics (routes, response times, memory, CPU, GC)
- Math operations via API and web interface
- Email notifications and extensions
- RESTful API structure with controllers, services, and models
- Database migrations with Alembic
- Docker support for easy deployment

## Project Structure

- `run.py` — Application entry point
- `app/`
  - `__init__.py` — App factory and setup
  - `database.py` — Database connection and models setup
  - `email_extension.py` — Email integration
  - `controllers/` — Route handlers (admin, auth, math, user, web, etc.)
  - `models/` — ORM models (user, admin request, log event, etc.)
  - `schemas/` — Marshmallow schemas for serialization
  - `services/` — Business logic (auth, user, admin, math, email)
  - `utils/` — Utilities and decorators
  - `static/` — Static files (CSS, JS)
  - `templates/` — HTML templates (dashboard, admin metrics, etc.)
- `migrations/` — Alembic migration scripts
- `tests/` — Unit and integration tests
- `requirements.txt` — Python dependencies
- `Dockerfile` — Docker image definition
- `docker-compose.yml` — Multi-container orchestration
