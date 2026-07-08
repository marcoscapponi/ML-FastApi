# ML API with FastAPI & Docker

Enterprise-ready machine learning API that unifies the full data -> model -> API -> database pipeline. Buiult with FastAPI, PostgreSQL(async), JWT authentication, Docker, and Alembic migrations. Designed to demonstrate professional backend skills for junior data/ML engineering interviews.

## Table of Contents

* [Architecture Overvierw]() (#architecture-overview)
* [Project Structure]() (#project-structure)
* [Tech Stack]() (#tech-stack)
* [Prerequisites]() (#prerequisites)
* [Quick Start (Docker)]() (#quick-start-docker)
* [Local Development]() (#local-development-setup)
* [Enviroment]() (#environment-variables)
* [Training the Model]() (#training-the-model)
* [Running the API]() (#running-the-api)
* [API Documentation &amp; Usage]() (#api-documentation--usage)
  * [Authentication]() (#authentication)
  * [Making Predictions]() (#making-predictions)
* [Database Management]()  (#database-management)
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

## Project Structure

ml-fastapi-project/
├── alembic/ # Database migrations
│ ├── versions/
│ └── env.py
├── scripts/
│ └── train_model.py # Model training & artifact creation
├── src/
│ ├── api/ # FastAPI routers & dependencies
│ │ └── v1/
│ ├── core/ # Config, security, exceptions
│ │ ├── config.py
│ │ └── security.py
│ ├── db/ # SQLAlchemy models & session
│ │ ├── base.py
│ │ └── session.py
│ ├── models/ # ML inference logic
│ │ ├── predict.py
│ │ └── artifacts/ # Saved model & metadata (gitignored)
│ ├── schemas/ # Pydantic request/response models
│ └── services/ # Business logic
├── tests/ # Unit & integration tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md

## Tech Stack

* **API**: FastAPI (Python 3.10+), uvicorn
* **Database**: PostgreSQL 16, SQLAlchemy 2.0 (async), asyncpg
* **Migrations: Alembic**
* **Authentication**: JWT (python-jose) + QAuth2, bcrypt (passlib)
* **ML**: scikit-learn (LogisticRegression), joblib, pandas
* **Validation**: Pydantic, email-validator
* **Containerization**: Docker, Docker Compose
* **Testing**: pytest, httpx, aiosqlite (for in-memory tests)
* **Code Quality**: Black, Ruff (pre-commit hooks)

## Prerequisites

* **Docker Desktop** (v20.10+) - for containerized deployment.
* **Python 3.10+** and **Poetry** - for local development.

## Quick Start (Docker)

1. Clone the repository and navigate into the project folder:
   ```
   git clone <your-repo-url>
   cd ml-fastapi-project
   ```
