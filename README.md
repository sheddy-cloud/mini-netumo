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
