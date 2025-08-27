from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base

class QRPermissionDtlsDB(Base):
    __tablename__ = 'qr_permission_dtls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qr_id = Column(UUID(as_uuid=True), ForeignKey("lost_and_found_qr.qr_id"), nullable=True)
    field_name = Column(String, nullable=True)
    permission = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    last_modified_date = Column(DateTime, nullable=True)
    active_status = Column(Boolean, default=True, nullable=True)
