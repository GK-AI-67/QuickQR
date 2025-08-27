from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.qr_service import QRCodeService
from app.models.qr_models import QRCodeRequest, QRCodeType, ErrorCorrectionLevel
from ..lost_and_found_qr.models.user_dtls_db import UserDtlsDB
from ..lost_and_found_qr.models.lost_and_found_qr_db import LostAndFoundQRDB
from ..lost_and_found_qr.models.user_qr_mpg_db import UserQRMPGDB
from ..lost_and_found_qr.models.lost_and_found_scanner_db import LostAndFoundScannerDB
from ..lost_and_found_qr.models.qr_permission_dtls_db import QRPermissionDtlsDB
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user_models import User
from ..core.logger import log_lost_and_found_event, log_api_request, lost_and_found_logger
from ..core.config import get_frontend_base_url

router = APIRouter(prefix="/lost-and-found", tags=["LostAndFound"])

# Admin user who can edit QR details on scan
ADMIN_USER_ID = "1c0aa08c-aae9-4634-9e88-3e0a5605bb99"

# Request models
class GenerateQRRequest(BaseModel):
    name: str

class UpdateQRDetailsRequest(BaseModel):
    qr_id: str
    user_id: Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str
    email: str
    address: str
    address_location: str
    description: str
    item_type: str
    permissions: Optional[Dict[str, str]] = None  # { field_name: 'visible' | 'hidden' }
    lock: Optional[bool] = True

class MarkFoundRequest(BaseModel):
    qr_id: str
    user_id: str
    found_location: str
    found_date: datetime

@router.post("/generate")
def generate_lost_and_found_qr(req: GenerateQRRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Resolve a user_dtls entry for the current user's email; create if missing
    
    user_id = current_user.userid
    # Log API request start
    log_api_request(
        endpoint="/lost-and-found/generate",
        method="POST",
        user_id=user_id,
        request_data={"name": req.name},
        level="INFO"
    )
    
    try:
        lost_and_found_logger.info(f"Starting QR generation for name: {req.name}, User ID: {user_id}")
        
        qr_id = uuid4()
        lost_and_found_logger.debug(f"Generated QR ID: {qr_id}")
        
        # Create QR record with just the name
        qr = LostAndFoundQRDB(
            qr_id=qr_id,
            name=req.name,
            first_name=None,
            last_name=None,
            phone_number=None,
            email=None,
            address=None,
            address_location=None,
            description=None,
            item_type=None,
            is_found=False,
            create_date=datetime.utcnow(),
            active_status=True
        )
        db.add(qr)
        lost_and_found_logger.debug(f"Added QR record to database: {qr_id}")
        
        # Create user-QR mapping
        mapping = UserQRMPGDB(
            qrid=qr_id,
            userid=user_id,
            details_updated=False,
            is_first_scan=True,
            scan_date=datetime.utcnow()
        )
        db.add(mapping)
        lost_and_found_logger.debug(f"Added user-QR mapping: User {user_id} -> QR {qr_id}")
        
        db.commit()
        lost_and_found_logger.info(f"Database commit successful for QR: {qr_id}")

        # Generate QR code pointing to the view URL
        qr_service = QRCodeService()
        base_url = get_frontend_base_url()
        view_url = f"{base_url}/lost-and-found/{qr_id}"
        qr_request = QRCodeRequest(
            content=view_url,
            qr_type=QRCodeType.URL,
            size=300,
            error_correction=ErrorCorrectionLevel.M,
            border=4,
            foreground_color="#000000",
            background_color="#FFFFFF",
            logo_url=None
        )
        
        lost_and_found_logger.debug(f"Generating QR code with service for ID: {qr_id}")
        qr_result = qr_service.generate_qr_code(qr_request, qr_id)
        qr_code_data = qr_result.get("qr_code_data")
        
        if not qr_code_data:
            raise Exception("QR code generation failed - no qr_code_data returned")
        
        lost_and_found_logger.info(f"QR code generated successfully for ID: {qr_id}")

        # Save the view URL in the database
        try:
            qr.qr_url = view_url
            db.commit()
            lost_and_found_logger.debug(f"Saved QR URL to DB for {qr_id}: {view_url}")
        except Exception as save_err:
            db.rollback()
            lost_and_found_logger.error(f"Failed to save QR URL for {qr_id}: {save_err}")
        
        # Log successful event
        log_lost_and_found_event(
            event_type="qr_generated",
            user_id=user_id,
            qr_id=str(qr_id),
            action="generate",
            details={"name": req.name, "qr_service_result": "success"}
        )
        
        # Log API request success
        log_api_request(
            endpoint="/lost-and-found/generate",
            method="POST",
            user_id=user_id,
            response_status=200,
            level="INFO"
        )
        
        return {
            "success": True, 
            "qr_code_data": qr_code_data, 
            "qr_id": str(qr_id),
            "view_url": view_url
        }
    except Exception as e:
        db.rollback()
        lost_and_found_logger.error(f"Error generating QR code: {str(e)}", exc_info=True)
        
        # Log error event
        log_lost_and_found_event(
            event_type="qr_generation_failed",
            user_id=user_id,
            action="generate",
            details={"name": req.name, "error": str(e)},
            error=e,
            level="ERROR"
        )
        
        # Log API request error
        log_api_request(
            endpoint="/lost-and-found/generate",
            method="POST",
            user_id=user_id,
            response_status=500,
            error=e,
            level="ERROR"
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-details")
def update_qr_details(req: UpdateQRDetailsRequest, db: Session = Depends(get_db)):
    # Log API request start
    log_api_request(
        endpoint="/lost-and-found/update-details",
        method="POST",
        user_id=req.user_id,
        request_data={"qr_id": req.qr_id, "first_name": req.first_name, "last_name": req.last_name},
        level="INFO"
    )
    
    try:
        lost_and_found_logger.info(f"Starting QR details update for QR ID: {req.qr_id}, User ID: {req.user_id}")
        
        # Convert string QR ID to UUID
        qr_uuid = UUID(req.qr_id)
        lost_and_found_logger.debug(f"Converted QR ID to UUID: {qr_uuid}")
        
        # Check if QR exists
        qr = db.query(LostAndFoundQRDB).filter_by(qr_id=qr_uuid).first()
        if not qr:
            lost_and_found_logger.warning(f"QR not found: {req.qr_id}")
            raise HTTPException(status_code=404, detail="QR not found")
        
        lost_and_found_logger.debug(f"Found QR record: {qr.name}")
        
        # If locked (permissions already exist), block further updates
        existing_perm = db.query(QRPermissionDtlsDB).filter_by(qr_id=qr_uuid).first()
        if existing_perm:
            raise HTTPException(status_code=409, detail="QR details are locked and cannot be updated")

        # Update QR details
        qr.first_name = req.first_name
        qr.last_name = req.last_name
        qr.phone_number = req.phone_number
        qr.email = req.email
        qr.address = req.address
        qr.address_location = req.address_location
        qr.description = req.description
        qr.item_type = req.item_type
        qr.last_modified_date = datetime.utcnow()
        
        lost_and_found_logger.debug(f"Updated QR details for: {req.qr_id}")
        
        # Create or update user-QR mapping
        if req.user_id:
            mapping = db.query(UserQRMPGDB).filter_by(
                qrid=qr_uuid, 
                userid=req.user_id
            ).first()
            
            if mapping:
                mapping.details_updated = True
                mapping.is_first_scan = False
                lost_and_found_logger.debug(f"Updated existing user-QR mapping for user: {req.user_id}")
            else:
                mapping = UserQRMPGDB(
                    qrid=qr_uuid,
                    userid=req.user_id,
                    details_updated=True,
                    is_first_scan=False,
                    scan_date=datetime.utcnow()
                )
                db.add(mapping)
                lost_and_found_logger.debug(f"Created new user-QR mapping for user: {req.user_id}")

        # Save permissions if provided (and lock)
        if req.permissions:
            # Clear any residual permissions (shouldn't exist as we blocked above)
            db.query(QRPermissionDtlsDB).filter_by(qr_id=qr_uuid).delete()
            for field_name, permission in req.permissions.items():
                db.add(QRPermissionDtlsDB(qr_id=qr_uuid, field_name=field_name, permission=permission))
        
        # Record scanner event
        scanner_event = LostAndFoundScannerDB(
            qrid=qr_uuid,
            userid=req.user_id,
            scan_type='update',
            action_taken='details_updated',
            create_date=datetime.utcnow()
        )
        db.add(scanner_event)
        lost_and_found_logger.debug(f"Added scanner event for QR: {req.qr_id}")
        
        db.commit()
        lost_and_found_logger.info(f"Database commit successful for QR details update: {req.qr_id}")
        
        # Log successful event
        log_lost_and_found_event(
            event_type="qr_details_updated",
            user_id=req.user_id,
            qr_id=req.qr_id,
            action="update_details",
            details={"has_contact_info": bool(req.phone_number and req.email)}
        )
        
        # Log API request success
        log_api_request(
            endpoint="/lost-and-found/update-details",
            method="POST",
            user_id=req.user_id,
            response_status=200,
            level="INFO"
        )
        
        return {"success": True, "message": "QR details updated successfully"}
        
    except Exception as e:
        db.rollback()
        lost_and_found_logger.error(f"Error updating QR details: {str(e)}", exc_info=True)
        
        # Log error event
        log_lost_and_found_event(
            event_type="qr_details_update_failed",
            user_id=req.user_id,
            qr_id=req.qr_id,
            action="update_details",
            details={"error": str(e)},
            error=e,
            level="ERROR"
        )
        
        # Log API request error
        log_api_request(
            endpoint="/lost-and-found/update-details",
            method="POST",
            user_id=req.user_id,
            response_status=500,
            error=e,
            level="ERROR"
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{qr_id}")
def get_lost_and_found_qr(qr_id: str, user_id: Optional[str] = None, lat: Optional[float] = None, lng: Optional[float] = None, db: Session = Depends(get_db), request: Request = None):
    # Log API request start
    log_api_request(
        endpoint=f"/lost-and-found/{qr_id}",
        method="GET",
        user_id=user_id,
        request_data={"qr_id": qr_id},
        level="INFO"
    )
    
    try:
        lost_and_found_logger.info(f"Starting QR retrieval for QR ID: {qr_id}, User ID: {user_id}")
        
        # Convert string QR ID to UUID
        qr_uuid = UUID(qr_id)
        lost_and_found_logger.debug(f"Converted QR ID to UUID: {qr_uuid}")
        
        # Check lock/permissions and mapping
        perms = db.query(QRPermissionDtlsDB).filter_by(qr_id=qr_uuid).all()
        is_locked = len(perms) > 0
        mapping = None
        if user_id:
            mapping = db.query(UserQRMPGDB).filter_by(
                qrid=qr_uuid, 
                userid=user_id
            ).first()
        
        lost_and_found_logger.debug(f"Existing mapping found: {mapping is not None}")
        
        # Get QR details
        qr = db.query(LostAndFoundQRDB).filter_by(qr_id=qr_uuid).first()
        if not qr:
            lost_and_found_logger.warning(f"QR not found: {qr_id}")
            raise HTTPException(status_code=404, detail="QR not found")
        
        lost_and_found_logger.debug(f"Found QR record: {qr.name}")

        # Decide UI mode for the scanning user
        can_edit = (user_id == ADMIN_USER_ID)
        ui_mode = "edit" if can_edit else "view"
        
        # Record scanner event
        scanner_event = LostAndFoundScannerDB(
            qrid=qr_uuid,
            userid=user_id,
            scan_type='view',
            action_taken='viewed_details',
            scanned_ip_address=request.client.host if request and request.client else None,
            scanned_user_agent=request.headers.get("user-agent") if request else None,
            create_date=datetime.utcnow()
        )
        if lat is not None and lng is not None:
            scanner_event.scanned_qr_location = f"{lat},{lng}"
        db.add(scanner_event)
        lost_and_found_logger.debug(f"Added scanner event for QR: {qr_id}")
        
        # If first time scanning for this user, create mapping
        if not mapping and user_id:
            mapping = UserQRMPGDB(
                qrid=qr_uuid,
                userid=user_id,
                is_first_scan=True,
                details_updated=False,
                scan_date=datetime.utcnow(),
                scan_ip=request.client.host if request and request.client else None,
                scan_user_agent=request.headers.get("user-agent") if request else None
            )
            db.add(mapping)
            db.commit()
            lost_and_found_logger.info(f"First time scan for QR: {qr_id}, User: {user_id}")
            
            # Log first scan event
            log_lost_and_found_event(
                event_type="first_scan",
                user_id=user_id,
                qr_id=qr_id,
                action="view",
                details={"qr_name": qr.name, "ip_address": request.client.host if request and request.client else None}
            )
            
            # Log API request success
            log_api_request(
                endpoint=f"/lost-and-found/{qr_id}",
                method="GET",
                user_id=user_id,
                response_status=200,
                level="INFO"
            )
            
            # For anonymous flow, treat first scan as needing edit when not locked
            if not is_locked:
                return {
                    "is_first_scan": True,
                    "qr_name": qr.name,
                    "message": "First time scan. Please update details.",
                    "has_details": False,
                    "can_edit": True if not user_id else can_edit,
                    "ui_mode": "edit" if not user_id else ui_mode
                }
            else:
                has_details = bool(qr.first_name and qr.last_name and qr.phone_number)
                return {
                    "is_first_scan": False,
                    "qr_name": qr.name,
                    "has_details": has_details,
                    "can_edit": can_edit,
                    "ui_mode": ui_mode,
                    "details": {
                        "first_name": qr.first_name,
                        "last_name": qr.last_name,
                        "phone_number": qr.phone_number,
                        "email": qr.email,
                        "address": qr.address,
                        "address_location": qr.address_location,
                        "description": qr.description,
                        "item_type": qr.item_type,
                        "is_found": qr.is_found,
                        "found_date": qr.found_date,
                        "found_location": qr.found_location
                    }
                }
        else:
            db.commit()
            lost_and_found_logger.debug(f"Subsequent scan for QR: {qr_id}, User: {user_id}")
            
            # Check if details are filled
            has_details = bool(qr.first_name and qr.last_name and qr.phone_number)
            lost_and_found_logger.debug(f"QR has details: {has_details}")
            
            # Log scan event
            log_lost_and_found_event(
                event_type="qr_scanned",
                user_id=user_id,
                qr_id=qr_id,
                action="view",
                details={"qr_name": qr.name, "has_details": has_details, "is_first_scan": False}
            )
            
            # Log API request success
            log_api_request(
                endpoint=f"/lost-and-found/{qr_id}",
                method="GET",
                user_id=user_id,
                response_status=200,
                level="INFO"
            )
            
            if has_details:
                # Apply permissions if present (reuse perms fetched above)
                visible = {p.field_name for p in perms if (p.permission or '').lower() == 'visible'} if perms else None
                full = {
                    "first_name": qr.first_name,
                    "last_name": qr.last_name,
                    "phone_number": qr.phone_number,
                    "email": qr.email,
                    "address": qr.address,
                    "address_location": qr.address_location,
                    "description": qr.description,
                    "item_type": qr.item_type,
                    "is_found": qr.is_found,
                    "found_date": qr.found_date,
                    "found_location": qr.found_location
                }
                details = full if not visible else {k: v for k, v in full.items() if k in visible}
                return {
                    "is_first_scan": False,
                    "qr_name": qr.name,
                    "has_details": True,
                    "can_edit": can_edit,
                    "ui_mode": ui_mode,
                    "details": details
                }
            else:
                return {
                    "is_first_scan": False,
                    "qr_name": qr.name,
                    "has_details": False,
                    "can_edit": can_edit,
                    "ui_mode": ui_mode,
                    "message": "Details not yet filled. Please update details."
                }
                
    except Exception as e:
        db.rollback()
        lost_and_found_logger.error(f"Error retrieving QR: {str(e)}", exc_info=True)
        
        # Log error event
        log_lost_and_found_event(
            event_type="qr_retrieval_failed",
            user_id=user_id,
            qr_id=qr_id,
            action="view",
            details={"error": str(e)},
            error=e,
            level="ERROR"
        )
        
        # Log API request error
        log_api_request(
            endpoint=f"/lost-and-found/{qr_id}",
            method="GET",
            user_id=user_id,
            response_status=500,
            error=e,
            level="ERROR"
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-found")
def mark_item_found(req: MarkFoundRequest, db: Session = Depends(get_db)):
    # Log API request start
    log_api_request(
        endpoint="/lost-and-found/mark-found",
        method="POST",
        user_id=req.user_id,
        request_data={"qr_id": req.qr_id, "found_location": req.found_location},
        level="INFO"
    )
    
    try:
        lost_and_found_logger.info(f"Starting mark found for QR ID: {req.qr_id}, User ID: {req.user_id}")
        
        # Convert string QR ID to UUID
        qr_uuid = UUID(req.qr_id)
        lost_and_found_logger.debug(f"Converted QR ID to UUID: {qr_uuid}")
        
        qr = db.query(LostAndFoundQRDB).filter_by(qr_id=qr_uuid).first()
        if not qr:
            lost_and_found_logger.warning(f"QR not found for mark found: {req.qr_id}")
            raise HTTPException(status_code=404, detail="QR not found")
        
        lost_and_found_logger.debug(f"Found QR record for mark found: {qr.name}")
        
        qr.is_found = True
        qr.found_date = req.found_date
        qr.found_location = req.found_location
        qr.found_by_user_id = req.user_id
        qr.last_modified_date = datetime.utcnow()
        
        lost_and_found_logger.debug(f"Updated QR as found: {req.qr_id}")
        
        # Record scanner event
        scanner_event = LostAndFoundScannerDB(
            qrid=qr_uuid,
            userid=req.user_id,
            scan_type='found',
            action_taken='marked_found',
            create_date=datetime.utcnow()
        )
        db.add(scanner_event)
        lost_and_found_logger.debug(f"Added scanner event for mark found: {req.qr_id}")
        
        db.commit()
        lost_and_found_logger.info(f"Database commit successful for mark found: {req.qr_id}")
        
        # Log successful event
        log_lost_and_found_event(
            event_type="item_marked_found",
            user_id=req.user_id,
            qr_id=req.qr_id,
            action="mark_found",
            details={"found_location": req.found_location, "found_date": str(req.found_date)}
        )
        
        # Log API request success
        log_api_request(
            endpoint="/lost-and-found/mark-found",
            method="POST",
            user_id=req.user_id,
            response_status=200,
            level="INFO"
        )
        
        return {"success": True, "message": "Item marked as found"}
        
    except Exception as e:
        db.rollback()
        lost_and_found_logger.error(f"Error marking item as found: {str(e)}", exc_info=True)
        
        # Log error event
        log_lost_and_found_event(
            event_type="mark_found_failed",
            user_id=req.user_id,
            qr_id=req.qr_id,
            action="mark_found",
            details={"error": str(e)},
            error=e,
            level="ERROR"
        )
        
        # Log API request error
        log_api_request(
            endpoint="/lost-and-found/mark-found",
            method="POST",
            user_id=req.user_id,
            response_status=500,
            error=e,
            level="ERROR"
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/qrs")
def get_user_qrs(user_id: str, db: Session = Depends(get_db)):
    # Log API request start
    log_api_request(
        endpoint=f"/lost-and-found/user/{user_id}/qrs",
        method="GET",
        user_id=user_id,
        level="INFO"
    )
    
    try:
        lost_and_found_logger.info(f"Starting user QRs retrieval for User ID: {user_id}")
        
        qrs = db.query(LostAndFoundQRDB).filter_by(
            user_id=user_id, 
            active_status=True
        ).all()
        
        lost_and_found_logger.debug(f"Found {len(qrs)} QRs for user: {user_id}")
        
        # Log successful event
        log_lost_and_found_event(
            event_type="user_qrs_retrieved",
            user_id=user_id,
            action="list_qrs",
            details={"qr_count": len(qrs)}
        )
        
        # Log API request success
        log_api_request(
            endpoint=f"/lost-and-found/user/{user_id}/qrs",
            method="GET",
            user_id=user_id,
            response_status=200,
            level="INFO"
        )
        
        return {
            "success": True,
            "qrs": [
                {
                    "qr_id": str(qr.qr_id),
                    "name": qr.name,
                    "is_found": qr.is_found,
                    "create_date": qr.create_date,
                    "found_date": qr.found_date
                }
                for qr in qrs
            ]
        }
    except Exception as e:
        lost_and_found_logger.error(f"Error retrieving user QRs: {str(e)}", exc_info=True)
        
        # Log error event
        log_lost_and_found_event(
            event_type="user_qrs_retrieval_failed",
            user_id=user_id,
            action="list_qrs",
            details={"error": str(e)},
            error=e,
            level="ERROR"
        )
        
        # Log API request error
        log_api_request(
            endpoint=f"/lost-and-found/user/{user_id}/qrs",
            method="GET",
            user_id=user_id,
            response_status=500,
            error=e,
            level="ERROR"
        )
        
        raise HTTPException(status_code=500, detail=str(e))
