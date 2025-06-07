import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Update this with PgBouncer connection string
user = os.getenv("PGBOUNCER_USER")
password = os.getenv("PGBOUNCER_PASSWORD")
database = os.getenv("DATABASE")

# PgBouncer connection string for SQLAlchemy (psycopg2)
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@pool:6432/{database}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
