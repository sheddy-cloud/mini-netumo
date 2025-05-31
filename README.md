# mini-netumo

A mini version of website monitoring platform like Netumo. It performs scheduled HTTP/HTTPS checks, monitors SSL and domain expiry, and sends alerts via email.

##  Features
- HTTP/HTTPS status and latency checks every 5 minutes
- SSL certificate expiry check (daily)
- Domain registration expiry check (daily)
- Alerts via email (Mailtrap)
- Vue front-end dashboard
- REST API with JWT authentication
- Docker Compose orchestration
- CI/CD with GitHub Actions + EC2 deployment

## Tech Stack
| Layer         | Technology               |
|---------------|---------------------------|
| API           | Python |
| Frontend      | Vue.js          |
| Background Jobs | Celery + Redis           |
| DB            | PostgreSQL               |
| Containerisation | Docker, Docker Compose  |
| Deployment    | AWS EC2 (t3micro)        |
| CI/CD         | GitHub Actions           |

## Deployment
### 1. Prerequisites
- AWS EC2 instance (t3.micro, Ubuntu)
- Docker & Docker Compose installed
- Open ports 80 (HTTP) and 443 (HTTPS)
  
### 2. Clone the Repository
```bash
git clone https://github.com/sheddy-cloud/mini-netumo.git
cd mini-netumo
