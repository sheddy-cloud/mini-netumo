# backend/tasks/tasks.py

import asyncio
import socket
import ssl
from datetime import datetime

import aiohttp
import whois
from api.database import get_db
from api.models.models import CertificateCheck, DomainCheck, StatusLog
from celery_app import celery_app

db = next(get_db())

# -------------------------------
# Task: Monitor target status
# -------------------------------

async def async_status_check(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            start = asyncio.get_event_loop().time()
            async with session.get(url, timeout=10) as response:
                end = asyncio.get_event_loop().time()
                return {
                    "status_code": response.status,
                    "latency_ms": round((end - start) * 1000),
                    "error": None
                }
        except Exception as e:
            return {
                "status_code": None,
                "latency_ms": None,
                "error": str(e)
            }


@celery_app.task(name="tasks.monitor_target")
def monitor_target(target_id: int, url: str):
    print(f"Running monitor_target for target_id={target_id}, url={url}")
    result = asyncio.run(async_status_check(url))
    timestamp = datetime.utcnow()

    try:
        log = StatusLog(
            target_id=target_id,
            status_code=result["status_code"],
            response_time_ms=result["latency_ms"],
            timestamp=timestamp
        )
        db.add(log)
        db.commit()
        print(f"📡 Status saved for Target {target_id} at {timestamp}")
    except Exception as e:
        db.rollback()
        print(f"⚠️ DB error: {e}")
    finally:
        db.close()
    return result


# -------------------------------
# Task: SSL & Domain Check
# -------------------------------

def get_ssl_expiry_date(hostname: str, port: int = 443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            return datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")


def get_domain_expiry(domain: str):
    try:
        w = whois.whois(domain)
        if isinstance(w.expiration_date, list):
            return w.expiration_date[0]
        return w.expiration_date
    except Exception as e:
        return str(e)


@celery_app.task(name="tasks.cert_check_target")
def cert_check_target(target_id: int, url: str):
    domain = url.split("//")[-1].split("/")[0]
    now = datetime.utcnow()

    try:
        # SSL check
        try:
            ssl_expiry = get_ssl_expiry_date(domain)
            ssl_days_left = (ssl_expiry - now).days
            cert_check = CertificateCheck(
                target_id=target_id,
                expiry_date=ssl_expiry,
                checked_at=now,
                days_remaining=ssl_days_left
            )
            db.add(cert_check)
        except Exception as e:
            print(f"🔐 SSL check failed: {e}")

        # WHOIS domain expiry
        try:
            domain_expiry = get_domain_expiry(domain)
            if isinstance(domain_expiry, datetime):
                domain_days_left = (domain_expiry - now).days
                domain_check = DomainCheck(
                    target_id=target_id,
                    expiry_date=domain_expiry,
                    checked_at=now,
                    days_remaining=domain_days_left
                )
                db.add(domain_check)
            else:
                print(f"📛 WHOIS failed: {domain_expiry}")
        except Exception as e:
            print(f"📛 WHOIS error: {e}")

        db.commit()
        print(f"✅ Cert/domain info saved for Target {target_id}")
    except Exception as e:
        db.rollback()
        print(f"❌ DB error: {e}")
    finally:
        db.close()
