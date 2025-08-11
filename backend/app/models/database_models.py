from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class QRDesign(Base):
    """Database model for storing QR code designs"""
    __tablename__ = "qr_designs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    qr_type = Column(String(50), nullable=False)
    size = Column(Integer, default=10)
    error_correction = Column(String(10), default="M")
    border = Column(Integer, default=4)
    foreground_color = Column(String(7), default="#000000")
    background_color = Column(String(7), default="#FFFFFF")
    logo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    content_data = relationship("ContentData", back_populates="qr_design", cascade="all, delete-orphan")
    images = relationship("DesignImage", back_populates="qr_design", cascade="all, delete-orphan")

class ContentData(Base):
    """Database model for storing content data associated with QR codes"""
    __tablename__ = "content_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    qr_design_id = Column(String, ForeignKey("qr_designs.id"), nullable=False)
    content_type = Column(String(50), nullable=False)  # 'text', 'image', 'text+image'
    text_content = Column(Text, nullable=True)
    image_filename = Column(String(255), nullable=True)
    image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    qr_design = relationship("QRDesign", back_populates="content_data")

class DesignImage(Base):
    """Database model for storing images associated with QR designs"""
    __tablename__ = "design_images"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    qr_design_id = Column(String, ForeignKey("qr_designs.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    image_data = Column(LargeBinary, nullable=True)  # For small images, store in DB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    qr_design = relationship("QRDesign", back_populates="images")

class QRCodeUsage(Base):
    """Database model for tracking QR code usage and analytics"""
    __tablename__ = "qr_code_usage"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    qr_design_id = Column(String, ForeignKey("qr_designs.id"), nullable=False)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String(500), nullable=True)
    referrer = Column(String(500), nullable=True)
    location = Column(String(100), nullable=True) 