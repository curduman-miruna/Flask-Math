# Flask-Math

Flask-Math is a Python web application that provides a dashboard for monitoring application metrics, user management, math operations, and admin features. The project uses Flask and is structured for modularity and scalability.
- Demo - https://www.youtube.com/watch?v=-cjFvipsvB0

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
  - `schemas/` — Pydantics schemas for serialization
  - `services/` — Business logic (auth, user, admin, math, email)
  - `utils/` — Utilities and decorators
    - `decorators/` — Custom decorators for routes
    - cache.py — Redis caching utilities
    - log_to_redis.py — Logging utilities for Redis
  - `static/` — Static files (CSS, JS)
  - `templates/` — HTML templates (dashboard, admin metrics, etc.)
- `migrations/` — Alembic migration scripts
- `requirements.txt` — Python dependencies
- `Dockerfile` — Docker image definition
- `docker-compose.yml` — Multi-container orchestration


## Tech Stack
- Python (Flask  framework)
- PostgreSQL (database)
- Redis (caching, logging)
- Prometheus (monitoring)
- JWT (authorization)
- Docker (containerization)

## Useful Links
- Flask Documentation: https://flask.palletsprojects.com/
- Async/Await in Flask: https://flask.palletsprojects.com/en/stable/async-await/
- Prometheus Flask Exporter: https://pypi.org/project/prometheus-flask-exporter/
- Prometheus Client: https://pypi.org/project/prometheus-client/
- Gmpy2 for Math Operations: https://gmpy2.readthedocs.io/en/latest/
- Pydantic for Data Validation: https://docs.pydantic.dev/
- Flask-Mail for Email: https://pythonhosted.org/Flask-Mail/
- Flask-Migrate for Database Migrations: https://flask-migrate.readthedocs.io/en/latest/
- Mailtrap for Email Sending: https://mailtrap.io/

