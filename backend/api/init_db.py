# backend/api/init_db.py

from api.database import Base, engine

# Create all tables defined in models
Base.metadata.create_all(bind=engine)

print("\u2705 Database tables created successfully.")
