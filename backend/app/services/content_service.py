import os
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.qr_models import QRContentDisplay, QRCodeType
from app.services.database_service import DatabaseService
from app.services.text_to_image_service import TextToImageService

class ContentService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.text_to_image_service = TextToImageService()
    
    async def save_content(self, 
                          content: str, 
                          qr_type: QRCodeType,
                          title: Optional[str] = None,
                          description: Optional[str] = None,
                          image_file: Optional[UploadFile] = None,
                          db: Session = None,
                          qr_id: Optional[str] = None) -> str:
        """Save content and return QR ID (uses provided qr_id when given)."""
        if not db:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                return await self._save_content_internal(content, qr_type, title, description, image_file, db, qr_id)
            finally:
                db.close()
        else:
            return await self._save_content_internal(content, qr_type, title, description, image_file, db, qr_id)
    
    async def _save_content_internal(self, 
                                   content: str, 
                                   qr_type: QRCodeType,
                                   title: Optional[str] = None,
                                   description: Optional[str] = None,
                                   image_file: Optional[UploadFile] = None,
                                   db: Session = None,
                                   qr_id: Optional[str] = None) -> str:
        """Internal method to save content with database session"""
        qr_id = qr_id or str(uuid.uuid4())
        
        # Determine content type and handle image creation
        content_type = "text"
        image_filename = None
        image_path = None
        
        if image_file:
            # Save uploaded image using database service
            design_image = await self.db_service.save_design_image(db, qr_id, image_file)
            image_filename = design_image.filename
            image_path = design_image.file_path
            content_type = "text+image" if content.strip() else "image"
        elif content.strip() and qr_type == "content":
            # Create text image for content type
            image_filename = self.text_to_image_service.create_text_image(
                text=content,
                title=title,
                description=description,
                qr_id=qr_id
            )
            image_path = f"/content/{image_filename}"
            content_type = "text"
        
        # Save content data to database
        self.db_service.save_content_data(
            db=db,
            qr_design_id=qr_id,
            content=content,
            content_type=content_type,
            image_filename=image_filename,
            image_path=image_path
        )
        
        return qr_id
    
    def get_content(self, qr_id: str, db: Session = None) -> Optional[QRContentDisplay]:
        """Get content by QR ID"""
        if not db:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                return self._get_content_internal(qr_id, db)
            finally:
                db.close()
        else:
            return self._get_content_internal(qr_id, db)
    
    def _get_content_internal(self, qr_id: str, db: Session) -> Optional[QRContentDisplay]:
        """Internal method to get content with database session"""
        content_data = self.db_service.get_content_data(db, qr_id)
        if not content_data:
            return None
        
        # Get QR design info
        qr_design = self.db_service.get_qr_design(db, qr_id)
        if not qr_design:
            return None
        
        # Get image URL if exists
        image_url = None
        if content_data.image_filename:
            if content_data.image_filename.endswith("_text.png"):
                # Text-generated image
                image_url = f"/content/{content_data.image_filename}"
            else:
                # Uploaded image
                image_url = f"/uploads/{content_data.image_filename}"
        
        return QRContentDisplay(
            qr_id=qr_id,
            title=qr_design.title,
            description=qr_design.description,
            content=content_data.text_content or "",
            content_type=content_data.content_type,
            image_url=image_url,
            created_at=qr_design.created_at,
            qr_type=qr_design.qr_type
        )
    
    def get_all_content(self, db: Session = None) -> List[QRContentDisplay]:
        """Get all content"""
        if not db:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                return self._get_all_content_internal(db)
            finally:
                db.close()
        else:
            return self._get_all_content_internal(db)
    
    def _get_all_content_internal(self, db: Session) -> List[QRContentDisplay]:
        """Internal method to get all content with database session"""
        qr_designs = self.db_service.get_all_qr_designs(db)
        content_list = []
        
        for design in qr_designs:
            content_data = self.db_service.get_content_data(db, design.id)
            if content_data:
                image_url = None
                if content_data.image_filename:
                    image_url = f"/uploads/{content_data.image_filename}"
                
                content_list.append(QRContentDisplay(
                    qr_id=design.id,
                    title=design.title,
                    description=design.description,
                    content=content_data.text_content or "",
                    content_type=content_data.content_type,
                    image_url=image_url,
                    created_at=design.created_at,
                    qr_type=design.qr_type
                ))
        
        return content_list
    
    def delete_content(self, qr_id: str, db: Session = None) -> bool:
        """Delete content by QR ID"""
        if not db:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                return self._delete_content_internal(qr_id, db)
            finally:
                db.close()
        else:
            return self._delete_content_internal(qr_id, db)
    
    def _delete_content_internal(self, qr_id: str, db: Session) -> bool:
        """Internal method to delete content with database session"""
        # Delete QR design (this will cascade delete related content and images)
        return self.db_service.delete_qr_design(db, qr_id) 