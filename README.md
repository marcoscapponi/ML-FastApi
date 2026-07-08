# ML API with FastAPI & Docker

Enterprise-ready machine learning API that unifies the full data -> model -> API -> database pipeline. Built with **FastAPI**, **PostgreSQL**(async), **JWT authentication**, **Docker**, and **Alembic** migrations. Designed to demonstrate professional backend skills for junior data/ML engineering interviews.

## Table of Contents

* [Architecture Overvierw]() (#architecture-overview)
* [Features]()(#features)
* [Project Structure]() (#project-structure)
* [Tech Stack]() (#tech-stack)
* [Prerequisites]() (#prerequisites)
* [Quick Start (Docker)]() (#quick-start-docker)
* [Local Development]() (#local-development-setup)
* [Enviroment]() (#environment-variables)
* [Database &amp; Migrations]()(#database--migratioins)
* [API Documentation &amp; Usage]() (#api-documentation--usage)
  * [Authentication]() (#authentication)
  * [User Profile]()(#user-profile)
  * [Making Predictions]() (#making-predictions)
  * [Prediction History]()(#prediction-history)
  * [Admin: Retrain Model]()(#admin-retrain-model)
* [Training the Model]() (#training-the-model)
* [Power BI Integration]()(#training-the-model)
* [Running Tests]() (#running-tests)
* [Code Quality &amp; Linting]() (#code-quality--linting)
* [Deployment Notes]()  (#deployment-notes)
* [License]() (#license)

## Architecture Overview

┌───────────┐ ┌──────────────┐ ┌─────────────┐ ┌────────────────┐
│ Data │────▶│ Training │────▶│ Serialized │────▶│ FastAPI App │
│ (CSV/DB) │ │ Script │ │ Model │ │ │
└───────────┘ └──────────────┘ └─────────────┘ └───────┬────────┘
│
┌──────▼────────┐
│ PostgreSQL │
│ (async) │
└───────────────┘

1. **Data Ingestion** - from a CSV file, database, or sklearn's built-in Iris dataset.
2. **Model training** - a Python script trains a `Logisticregresion` classifier,
   preprocesses features with `StandardScaler`, and saves both model and scaler.
3. **API layer** - FastAPI loads the model at startup and exposes a secure REST API.
4. **Database** - user credentials (hashed) and prediction history are stored in
   PostgreSQL using async SQLAlchemy.
5. **Admin endpoint** - allows an administrator to trigger model retraining from the API itself.

## Features

- JWT authentication with OAuth2 password flow (register, login, protected routes)
- Machine learning inference (Logistic Regression on Iris dataset)
- Prediction history with desnormalized columns for analytics (`class_name`, `sepal_lengrh`, `sepal_width`, `petal_length`, `petal_width`, `probability`)
- Full integration with **Power BI** via Python script (auto-login, fetch history)
- Unit and integration tests with `pytest` (SQLite in-memory for tests)
- Dockerized with multi-stage builds and Docker Compose
- Alembic migrations for database schema versioning
- Admin endpoint for model retraining
- Automatic interactive API docs (Swagger UI and ReDoc)
- CI/CD workflow with GitHub Actions

## Project Structure

ml-fastapi-project/
├── .github/
│ └── workflows/
│ └── tests.yml # CI pipeline
├── alembic/ # Database migrations
│ ├── versions/
│ │ ├── 0001_initial_users_predictions.py
│ │ ├── 0002_add_columns_to_predictions.py
│ │ └── 0003_add_is_admin_to_users.py
│ └── env.py
├── scripts/
│ └── train_model.py # Model training & artifact creation
├── src/
│ ├── api/
│ │ └── v1/
│ │ ├── endpoints/
│ │ │ ├── auth.py
│ │ │ ├── users.py
│ │ │ ├── predictions.py
│ │ │ └── admin.py # Retrain endpoint
│ │ ├── dependencies.py # get_current_user
│ │ └── router.py
│ ├── core/
│ │ ├── config.py # Pydantic settings from env
│ │ ├── security.py # JWT and hashing
│ │ └── exceptions.py # Global error handlers
│ ├── db/
│ │ ├── base.py # SQLAlchemy models & engine
│ │ ├── session.py # Async session dependency
│ │ └── repositories/ # (optional) repository pattern
│ ├── models/
│ │ ├── artifacts/ # Saved model & metadata (gitignored)
│ │ └── predict.py # Inference logic
│ ├── schemas/
│ │ ├── user.py
│ │ ├── token.py
│ │ └── prediction.py
│ ├── services/
│ │ ├── auth_service.py
│ │ ├── user_service.py
│ │ └── prediction_service.py
│ └── main.py # FastAPI application entry point
├── tests/
│ ├── conftest.py # Fixtures (DB, client, auth)
│ ├── test_auth.py
│ ├── test_users.py
│ ├── test_predictions.py
│ └── test_models/
│ └── test_model.py
├── examples/
│ └── api_usage.ipynb # Jupyter notebook with API usage & extra model
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md

## Tech Stack

* **API**: FastAPI (Python 3.10+), uvicorn
* **Database**: PostgreSQL 16, SQLAlchemy 2.0 (async), asyncpg
* **Migrations:** Alembic
* **Authentication**: JWT (python-jose) + OAuth2, bcrypt (passlib)
* **ML**: scikit-learn (LogisticRegression), joblib, pandas
* **Validation**: Pydantic, email-validator
* **Containerization**: Docker, Docker Compose
* **Testing**: pytest, httpx, aiosqlite (for in-memory tests)
* **Code Quality**: Black, Ruff (pre-commit hooks)
* **CI**:GitHub Actions

## Prerequisites

* **Docker Desktop** (v20.10+) - for running tha application and for containerized deployment.
* **Python 3.10+** and **Poetry** - for local development.
* **Power  BI Desktop** - for dashboard integration

## Quick Start (Docker)

1. Clone the repository and navigate into the project folder:
   ```
   git clone <your-repo-url>
   cd ml-fastapi-project
   ```
