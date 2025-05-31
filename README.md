# mini-netumo


A mini version of website monitoring platform like Netumo. It performs scheduled HTTP/HTTPS checks, monitors SSL and domain expiry, and sends alerts via email.

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
