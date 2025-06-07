import time

from api.database import Base, engine
from api.models import (Alert, CertificateCheck, DomainCheck, StatusLog,
                        Target, User)
from sqlalchemy.exc import OperationalError

MAX_RETRIES = 10
RETRY_DELAY = 5  # seconds

def init_db():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"🔄 Attempt {attempt}: Trying to create database tables...")
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully.")
            break
        except OperationalError as e:
            print(f"⚠️  Attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"⏳ Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("❌ Could not connect to the database after multiple attempts.")
                raise

init_db()
