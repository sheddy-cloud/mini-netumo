# Mini-Netumo

A lightweight clone of Netumo to monitor website uptime, SSL, and domain expiry. Sends alerts via email and displays metrics on a dashboard.

---

## Features

-  HTTP/HTTPS status and latency checks every 5 minutes
-  SSL certificate expiry check (daily)
-  Domain registration expiry check (daily)
-  Alerts via email (Mailtrap)
-  Front-end dashboard with status, latency and expiry countdown
-  REST API with JWT authentication and Swagger docs
-  Containerised via Docker Compose
-  CI/CD with GitHub Actions + AWS EC2 deployment

---

##  Tech Stack

| Layer              | Technology                |
|-------------------|---------------------------|
| API               | Python (FastAPI) or Node.js |
| Frontend          | React or Vue.js            |
| Background Jobs   | Celery + Redis             |
| Notification Queue| Redis                      |
| DB                | PostgreSQL                 |
| Containerisation  | Docker, Docker Compose     |
| Deployment        | AWS EC2 (t3.micro)         |
| CI/CD             | GitHub Actions             |

---

##  Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/sheddy-cloud/mini-netumo.git
cd mini-netumo
````

### 2. Create `.env` File

```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=mini_netumo
JWT_SECRET=your_jwt_secret
MAILTRAP_USERNAME=your_mailtrap_user
MAILTRAP_PASSWORD=your_mailtrap_pass
```

### 3. Build and Start Services

```bash
docker-compose up --build
```

### 4. Access Services

* Frontend: `http://localhost`
* API: `http://localhost/api`
* Swagger Docs: `http://localhost/api/docs`

---

##  API Endpoints

* `POST /targets/` – Add new website to monitor
* `GET /status/{id}` – Current status of a site
* `GET /history/{id}` – Past monitoring logs
* `GET /alerts/` – Triggered alert list

Secured via JWT tokens.

---

##  Alerts

Alerts are triggered when:

* Two consecutive HTTP checks fail
* SSL or domain expires in ≤ 14 days

Delivery:

* Email (Mailtrap/SES)

---

##  Live Deployment

> [View Live on EC2](http://<your-ec2-public-ip-or-dns>)

---

##  Team

| Name     | Role     |
| -------- | -------- |
| Witnes  | Frontend |
| shadrack | Backend  |
| josephat | DevOps   |
| hassan   | Backen   |
| furahini | Frontend |

---

##  Project Structure

```
.
├── api/                  # REST API
├── frontend/             # Vue dashboard
├── workers/
│   ├── monitoring/       # Periodic HTTP/SSL/WHOIS checks
│   └── notifications/    # Alert queue consumers
├── redis/                # Redis config
├── nginx/                # Load balancer config
├── docker-compose.yml
├── .github/workflows/    # CI/CD pipeline
└── README.md
```

---

##  Testing & Logs

* Logs: `docker-compose logs -f`
* Log rotation recommended (e.g., to Loki/Grafana Cloud)
* Run tests via GitHub Actions on each commit

---

##  Screenshots

* `screenshots/docker_ps.png` – Docker container status
* `screenshots/alert-email.png` – Example email alert


---

##  Database & Backup

* Uses PostgreSQL with connection pooling
* Auto-backup: `artefact_bundle/db_backup.sql.gz`

---

##  Submission Artefacts

* `screenshots/`
* `logs/`
* `db_backup.sql.gz`




## Features
- HTTP/HTTPS status and latency checks every 5 minutes
- SSL certificate expiry check (daily)
- Domain registration expiry check (daily)
- Alerts via email (Mailtrap)
- Vue front-end dashboard
- REST API with JWT authentication
- Docker Compose orchestration
- CI/CD with GitHub Actions + EC2 deployment

## Dev Tools

### Pre-commit
Automate code linting with pre-commit.

1. Install pre-commit (if not already)
```bash
pip install pre-commit
```

2. Install the hooks into your Git repo:
```bash
pre-commit install
```

3. Run it manually before commit (optional):

```bash
pre-commit run --all-files
```
