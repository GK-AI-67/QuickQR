from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class LostAndFoundQRDB(Base):
    __tablename__ = 'lost_and_found_qr'
    qr_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=True)  # QR name given by user
    user_id = Column(String(255), nullable=True)
    qr_url = Column(String(500), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    address_location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)  # Additional details about the item
    item_type = Column(String(100), nullable=True)  # Type of item (phone, wallet, etc.)
    is_found = Column(Boolean, default=False, nullable=True)  # Whether item has been found
    found_date = Column(DateTime, nullable=True)  # When item was found
    found_location = Column(String(255), nullable=True)  # Where item was found
    found_by_user_id = Column(String(255), nullable=True)  # Who found the item
    create_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    last_modified_date = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    active_status = Column(Boolean, default=True, nullable=True)
