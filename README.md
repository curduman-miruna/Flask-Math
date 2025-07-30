# Flask-Math

Flask-Math is a Python web application that provides a dashboard for monitoring application metrics, user access management, math operations, and admin features. The project uses Flask and is structured for modularity and scalability.
- Demo - https://www.youtube.com/watch?v=-cjFvipsvB0

## Features

- User authentication and authorization with JWT: 
  - Login and registration
  - User roles (admin, user, superadmin)
- Admin request management:
  - Dashboard for admin requests for user to access metrics
  - Superadmin approval for admin requests
- Monitoring and metrics:
  - Admin dashboard with application metrics (routes, response times, memory, CPU, GC)
  - Prometheus integration for monitoring
- Math operations via API and web interface
  - Advanced math operations using gmpy2
  - Result cached in Redis for 60 minutes
  - 2 forms for math results:
    - scientific notation: `1.23456789e+10`
    - string representation: `12345678900`
- Email verification:
  - Flask-Mail for sending emails
  - Only verified users can request admin access
- RESTful API structure with controllers, services, and models
  - Controllers for handling routes
  - Services for business logic
  - Models for database interactions
  - Schemas for data validation and serialization using Pydantic:
    - User schema
    - Admin request schema
    - Math operation schema
- Logging and caching:
  - Redis for caching math results
  - Redis for logging events
  - PostgreSQL for persistent API_CALL logs

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

