from datetime import datetime, timezone

from api.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# ----------------------------- SQLAlchemy Models -----------------------------


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    alerts = relationship("Alert", back_populates="user")
    targets = relationship("Target", back_populates="user")



class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sent_at = Column(DateTime)
    type = Column(String)
    message = Column(Text)
    user = relationship("User", back_populates="alerts")


class Target(Base):
    __tablename__ = "targets"
    target_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    check_interval = Column(Integer)
    enabled = Column(Integer)
    created_at = Column(DateTime)
    user = relationship("User", back_populates="targets")
    status_logs = relationship("StatusLog", back_populates="target")
    domain_checks = relationship("DomainCheck", back_populates="target")
    certificate_checks = relationship("CertificateCheck", back_populates="target")


class StatusLog(Base):
    __tablename__ = "statuslogs"
    log_id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.target_id"))
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    timestamp = Column(DateTime)
    target = relationship("Target", back_populates="status_logs")


class DomainCheck(Base):
    __tablename__ = "domainchecks"
    domain_id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.target_id"))
    expiry_date = Column(DateTime)
    checked_at = Column(DateTime)
    days_remaining = Column(Integer)
    target = relationship("Target", back_populates="domain_checks")


class CertificateCheck(Base):
    __tablename__ = "certificatechecks"
    cert_id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.target_id"))
    expiry_date = Column(DateTime)
    checked_at = Column(DateTime)
    days_remaining = Column(Integer)
    target = relationship("Target", back_populates="certificate_checks")
