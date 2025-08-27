from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class LostAndFoundScannerDB(Base):
    __tablename__ = 'lost_and_found_scanner'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    qrid = Column(UUID(as_uuid=True), ForeignKey("lost_and_found_qr.qr_id"), nullable=True)  # which qr is scanned
    userid = Column(String(255), nullable=True)  # who scans the qr
    scanned_qr_location = Column(String(255), nullable=True)  # longitude and latitude
    scanned_ip_address = Column(String(45), nullable=True)  # IP address of scanner
    scanned_user_agent = Column(Text, nullable=True)  # Browser/device info
    scan_type = Column(String(50), default='view', nullable=True)  # 'view', 'update', 'found'
    action_taken = Column(String(100), nullable=True)  # What action was taken
    create_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    active_status = Column(Boolean, default=True, nullable=True)
