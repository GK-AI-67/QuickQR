from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional, Dict, Any
from app.models.database_models import QRDesign, ContentData, DesignImage, QRCodeUsage
from app.models.qr_models import QRCodeRequest, QRCodeType, ContactQRDisplay
from app.core.database import get_db
import os
import uuid
from datetime import datetime
import aiofiles
from fastapi import UploadFile

class DatabaseService:
    """Service for handling database operations related to QR designs"""
    
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def create_qr_design(self, db: Session, qr_request: Dict[str, Any], qr_id: Optional[str] = None) -> QRDesign:
        """Create a new QR design in the database"""
        design = QRDesign(
            id=qr_id or str(uuid.uuid4()),
            title=qr_request.get('title'),
            description=qr_request.get('description'),
            content=qr_request.get('content'),
            qr_type=qr_request.get('qr_type'),
            size=qr_request.get('size'),
            error_correction=qr_request.get('error_correction'),
            border=qr_request.get('border'),
            foreground_color=qr_request.get('foreground_color'),
            background_color=qr_request.get('background_color'),
            logo_url=qr_request.get('logo_url')
        )
        
        db.add(design)
        db.commit()
        db.refresh(design)
        return design
    
    def get_qr_design(self, db: Session, design_id: str) -> Optional[QRDesign]:
        """Get a QR design by ID"""
        return db.query(QRDesign).filter(
            and_(QRDesign.id == design_id, QRDesign.is_active == True)
        ).first()
    
    def get_all_qr_designs(self, db: Session, limit: int = 100, offset: int = 0) -> List[QRDesign]:
        """Get all QR designs with pagination"""
        return db.query(QRDesign).filter(
            QRDesign.is_active == True
        ).order_by(desc(QRDesign.created_at)).offset(offset).limit(limit).all()
    
    def update_qr_design(self, db: Session, design_id: str, update_data: Dict[str, Any]) -> Optional[QRDesign]:
        """Update a QR design"""
        design = self.get_qr_design(db, design_id)
        if not design:
            return None
        
        for key, value in update_data.items():
            if hasattr(design, key):
                setattr(design, key, value)
        
        design.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(design)
        return design
    
    def delete_qr_design(self, db: Session, design_id: str) -> bool:
        """Soft delete a QR design"""
        design = self.get_qr_design(db, design_id)
        if not design:
            return False
        
        design.is_active = False
        db.commit()
        return True
    
    def save_content_data(self, db: Session, qr_design_id: str, content: str, 
                         content_type: str, image_filename: Optional[str] = None,
                         image_path: Optional[str] = None) -> ContentData:
        """Save content data associated with a QR design"""
        content_data = ContentData(
            qr_design_id=qr_design_id,
            content_type=content_type,
            text_content=content,
            image_filename=image_filename,
            image_path=image_path
        )
        
        db.add(content_data)
        db.commit()
        db.refresh(content_data)
        return content_data
    
    def get_content_data(self, db: Session, qr_design_id: str) -> Optional[ContentData]:
        """Get content data for a QR design"""
        return db.query(ContentData).filter(
            ContentData.qr_design_id == qr_design_id
        ).first()
    
    async def save_design_image(self, db: Session, qr_design_id: str, 
                               image_file: UploadFile) -> DesignImage:
        """Save an image file associated with a QR design"""
        # Generate unique filename
        file_extension = os.path.splitext(image_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file to disk
        async with aiofiles.open(file_path, 'wb') as f:
            content = await image_file.read()
            await f.write(content)
        
        # Create database record
        design_image = DesignImage(
            qr_design_id=qr_design_id,
            filename=unique_filename,
            original_filename=image_file.filename,
            file_path=file_path,
            file_size=len(content),
            mime_type=image_file.content_type or "application/octet-stream"
        )
        
        db.add(design_image)
        db.commit()
        db.refresh(design_image)
        return design_image
    
    def get_design_images(self, db: Session, qr_design_id: str) -> List[DesignImage]:
        """Get all images for a QR design"""
        return db.query(DesignImage).filter(
            DesignImage.qr_design_id == qr_design_id
        ).all()
    
    def delete_design_image(self, db: Session, image_id: str) -> bool:
        """Delete a design image"""
        image = db.query(DesignImage).filter(DesignImage.id == image_id).first()
        if not image:
            return False
        
        # Delete file from disk
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        
        db.delete(image)
        db.commit()
        return True
    
    def record_qr_usage(self, db: Session, qr_design_id: str, 
                       ip_address: Optional[str] = None,
                       user_agent: Optional[str] = None,
                       referrer: Optional[str] = None,
                       location: Optional[str] = None) -> QRCodeUsage:
        """Record QR code usage for analytics"""
        usage = QRCodeUsage(
            qr_design_id=qr_design_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            location=location
        )
        
        db.add(usage)
        db.commit()
        db.refresh(usage)
        return usage
    
    def get_qr_usage_stats(self, db: Session, qr_design_id: str) -> Dict[str, Any]:
        """Get usage statistics for a QR design"""
        total_scans = db.query(QRCodeUsage).filter(
            QRCodeUsage.qr_design_id == qr_design_id
        ).count()
        
        recent_scans = db.query(QRCodeUsage).filter(
            QRCodeUsage.qr_design_id == qr_design_id
        ).order_by(desc(QRCodeUsage.scanned_at)).limit(10).all()
        
        return {
            "total_scans": total_scans,
            "recent_scans": [
                {
                    "scanned_at": scan.scanned_at,
                    "ip_address": scan.ip_address,
                    "user_agent": scan.user_agent
                }
                for scan in recent_scans
            ]
        }
    
    def search_qr_designs(self, db: Session, query: str, limit: int = 50) -> List[QRDesign]:
        """Search QR designs by title, description, or content"""
        search_term = f"%{query}%"
        return db.query(QRDesign).filter(
            and_(
                QRDesign.is_active == True,
                (
                    QRDesign.title.ilike(search_term) |
                    QRDesign.description.ilike(search_term) |
                    QRDesign.content.ilike(search_term)
                )
            )
        ).order_by(desc(QRDesign.created_at)).limit(limit).all() 

    def save_contact_qr_data(self, db: Session, contact_data: ContactQRDisplay) -> ContactQRDisplay:
        """Save Contact QR data to database"""
        # For now, we'll store it in the content_data table with a special type
        # In a production app, you'd have a dedicated ContactQR table
        content_data = ContentData(
            qr_design_id=contact_data.qr_id,
            content_type="contact_qr",
            text_content=str(contact_data.dict()),
            image_filename=None,
            image_path=None
        )
        
        db.add(content_data)
        db.commit()
        db.refresh(content_data)
        return contact_data
    
    def get_contact_qr_data(self, db: Session, qr_id: str) -> Optional[ContactQRDisplay]:
        """Get Contact QR data from database"""
        content_data = db.query(ContentData).filter(
            and_(ContentData.qr_design_id == qr_id, ContentData.content_type == "contact_qr")
        ).first()
        
        if not content_data:
            return None
        
        try:
            # Parse the stored contact data
            import ast
            contact_dict = ast.literal_eval(content_data.text_content)
            return ContactQRDisplay(**contact_dict)
        except:
            # Fallback: create basic contact data
            return ContactQRDisplay(
                qr_id=qr_id,
                full_name="Contact Information",
                phone_number="Available",
                address="Available",
                created_at=content_data.created_at,
                qr_type="contact_qr"
            ) 