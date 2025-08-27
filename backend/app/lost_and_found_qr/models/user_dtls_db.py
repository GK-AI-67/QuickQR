from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class UserDtlsDB(Base):
    __tablename__ = 'user_dtls'
    userid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    gmail = Column(String(255), nullable=True, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=True)
    last_logged_in_time = Column(DateTime, nullable=True)
    active_status = Column(Boolean, default=True, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    provider = Column(String(50), default="local", nullable=True)  # local | google
