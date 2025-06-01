# Mini-Netumo Backend API

## Overview

Mini-Netumo Backend API is a RESTful API built with FastAPI and SQLAlchemy for managing users, targets, alerts, status logs, domain checks, and certificate checks. It is designed for monitoring and alert systems with secure and scalable data handling.

---

## Features

- User management (create, read, update)
- Target management (create, read, update)
- Alert management (create, read, update)
- Status log recording
- Domain check management
- Certificate check management
- SQLite database for data persistence
- Modular API structure using FastAPI routers

---

## Project Structure

project/
│
├── main.py # FastAPI app entry point
├── database.py # Database engine and session setup
├── init_db.py # Script to initialize the database tables
├── models/
│ └── models.py # SQLAlchemy ORM models
├── schemas/
│ ├── user.py # Pydantic schemas for User entity
│ ├── target.py # Pydantic schemas for Target entity
│ ├── alert.py # Pydantic schemas for Alert entity
│ ├── statuslog.py # Pydantic schemas for StatusLog entity
│ ├── domaincheck.py # Pydantic schemas for DomainCheck entity
│ └── certificatecheck.py # Pydantic schemas for CertificateCheck entity
├── routers/
│ ├── user.py # API endpoints related to Users
│ ├── target.py # API endpoints related to Targets
│ ├── alert.py # API endpoints related to Alerts
│ ├── statuslog.py # API endpoints related to StatusLogs
│ ├── domaincheck.py # API endpoints related to DomainChecks
│ └── certificatecheck.py # API endpoints related to CertificateChecks
└── utils/
└── security.py # Utility functions (e.g., password hashing)


---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mini-netumo-backend.git
cd mini-netumo-backend/backend/api

# Create and activate a virtual environment (recommended)

# Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

# Initialize the database (run once)
python init_db.py
# OR 
python -m api.init_db (preferred)

# Run the FastAPI server
python uvicorn main:app --reload 
# OR 
uvicorn main:app --reload
# OR
python -m uvicorn main:app --port 8001

# Access the API documentation
http://127.0.0.1:8000/docs


API Endpoints Summary
Users
POST /users/ — Create a new user

GET /users/ — List users with pagination

GET /users/{user_id} — Get user details by ID

PUT /users/{user_id} — Update user info

Targets
POST /targets/ — Create a new target

GET /targets/ — List targets

GET /targets/{target_id} — Get target details by ID

PUT /targets/{target_id} — Update target

Alerts
POST /alerts/ — Create a new alert (typically created by system/machines)

GET /alerts/ — List alerts

GET /alerts/{alert_id} — Get alert by ID

PUT /alerts/{alert_id} — Update alert

Status Logs
POST /statuslogs/ — Create a status log entry

GET /statuslogs/ — List status logs

Domain Checks
POST /domainchecks/ — Create domain check record

GET /domainchecks/ — List domain checks

Certificate Checks
POST /certificatechecks/ — Create certificate check record

GET /certificatechecks/ — List certificate checks

# Notes
Passwords are securely hashed before storing.

Timestamps are handled in UTC for consistency.

SQLite is used for simplicity but you can configure other databases in database.py.

Alerts and monitoring logs are generally created automatically by the system rather than manually by users.

# Contributing
Feel free to fork the repo, open issues, or submit pull requests.

# Contact
If you have questions or want to contribute, contact:

Email: hassanjemadari@gmail.com

GitHub: https://github.com/jemadari