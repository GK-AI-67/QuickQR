from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class UserQRMPGDB(Base):
    __tablename__ = 'user_qr_mpg'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qrid = Column(UUID(as_uuid=True), ForeignKey("lost_and_found_qr.qr_id"), nullable=True)  # QR ID
    userid = Column(String(255), nullable=True)  # User ID who scanned
    scan_location = Column(String(255), nullable=True)  # GPS coordinates when scanned
    scan_ip = Column(String(45), nullable=True)  # IP address of scanner
    scan_user_agent = Column(Text, nullable=True)  # Browser/device info
    scan_date = Column(DateTime, default=datetime.utcnow, nullable=True)  # When QR was scanned
    is_first_scan = Column(Boolean, default=True, nullable=True)  # Whether this is the first scan
    details_updated = Column(Boolean, default=False, nullable=True)  # Whether details were updated
    created_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    active_status = Column(Boolean, default=True, nullable=True)
