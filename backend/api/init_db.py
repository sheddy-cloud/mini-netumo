# backend/api/init_db.py

from api.database import Base, engine
from api.models import (Alert, CertificateCheck, DomainCheck,  # 👈 Necessary!
                        StatusLog, Target, User)

# Create all tables defined in models
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully.")
