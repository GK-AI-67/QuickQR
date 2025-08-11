from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.qr_models import (
    QRCodeRequest, QRCodeResponse, AISuggestionRequest, AISuggestionResponse, QRContentDisplay
)
from app.services.qr_service import QRCodeService
from app.services.ai_service import AIService
from app.services.content_service import ContentService
from app.services.database_service import DatabaseService
from app.core.database import get_db
from app.api.auth import get_current_user

# Create routers
qr_router = APIRouter()
ai_router = APIRouter()
content_router = APIRouter()

# Initialize services
qr_service = QRCodeService()
ai_service = AIService()
content_service = ContentService()
db_service = DatabaseService()

# Pydantic model for content generation request
class ContentGenerationRequest(BaseModel):
    prompt: str
    include_images: bool = False

@qr_router.post("/generate", response_model=QRCodeResponse)
async def generate_qr_code(request: QRCodeRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate a QR code with the specified parameters"""
    try:
        # Validate content
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        # Save QR design to database
        qr_design = db_service.create_qr_design(db, request)
        qr_id = qr_design.id
        
        # For content type, save content data
        if request.qr_type == "content":
            await content_service.save_content(
                content=request.content,
                qr_type=request.qr_type,
                title=request.title,
                description=request.description,
                db=db
            )
            
            # Get the content data to find image URL
            content_data = content_service.get_content(qr_id, db)
            image_url = content_data.image_url if content_data else None
        else:
            image_url = None
        
        # Generate QR code
        result = qr_service.generate_qr_code(request, qr_id, image_url)
        
        if result["success"]:
            return QRCodeResponse(
                success=True,
                qr_code_data=result["qr_code_data"],
                qr_id=qr_id,
                view_url=result.get("view_url"),
                metadata=result["metadata"]
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@qr_router.post("/generate-with-image", response_model=QRCodeResponse)
async def generate_qr_code_with_image(
    content: str = Form(...),
    qr_type: str = Form("content"),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Generate a QR code with image upload"""
    try:
        # Validate content
        if not content.strip() and not image_file:
            raise HTTPException(status_code=400, detail="Content or image is required")
        
        # Create QR request
        qr_request = QRCodeRequest(
            content=content,
            qr_type=qr_type,
            title=title,
            description=description
        )
        
        # Save QR design to database
        qr_design = db_service.create_qr_design(db, qr_request)
        qr_id = qr_design.id
        
        # Save content with image
        await content_service.save_content(
            content=content,
            qr_type=qr_type,
            title=title,
            description=description,
            image_file=image_file,
            db=db
        )
        
        # Get the content data to find image URL
        content_data = content_service.get_content(qr_id, db)
        image_url = content_data.image_url if content_data else None
        
        # Generate QR code
        result = qr_service.generate_qr_code(qr_request, qr_id, image_url)
        
        if result["success"]:
            return QRCodeResponse(
                success=True,
                qr_code_data=result["qr_code_data"],
                qr_id=qr_id,
                view_url=result.get("view_url"),
                metadata=result["metadata"]
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@qr_router.get("/types")
async def get_qr_types():
    """Get available QR code types"""
    return {
        "types": [
            {"value": "url", "label": "URL", "description": "Website links"},
            {"value": "text", "label": "Text", "description": "Plain text content"},
            {"value": "contact", "label": "Contact", "description": "Contact information (vCard)"},
            {"value": "wifi", "label": "WiFi", "description": "WiFi network credentials"},
            {"value": "email", "label": "Email", "description": "Email address"},
            {"value": "phone", "label": "Phone", "description": "Phone number"},
            {"value": "sms", "label": "SMS", "description": "Text message"}
        ]
    }

@qr_router.get("/error-correction-levels")
async def get_error_correction_levels():
    """Get available error correction levels"""
    return {
        "levels": [
            {"value": "L", "label": "Low (7%)", "description": "Lowest error correction"},
            {"value": "M", "label": "Medium (15%)", "description": "Default level"},
            {"value": "Q", "label": "Quartile (25%)", "description": "Higher error correction"},
            {"value": "H", "label": "High (30%)", "description": "Highest error correction"}
        ]
    }

@qr_router.post("/validate-url")
async def validate_url(url: str):
    """Validate URL format"""
    is_valid = qr_service.validate_url(url)
    return {
        "url": url,
        "is_valid": is_valid,
        "suggestions": [] if is_valid else ["Add https:// protocol", "Check URL format"]
    }

@ai_router.post("/suggestions", response_model=AISuggestionResponse)
async def get_ai_suggestions(request: AISuggestionRequest):
    """Get AI-powered suggestions for QR code content"""
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        result = await ai_service.get_suggestions(
            request.content, 
            request.qr_type, 
            request.context
        )
        
        return AISuggestionResponse(
            suggestions=result["suggestions"],
            optimized_content=result["optimized_content"],
            confidence_score=result["confidence_score"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI suggestions: {str(e)}")

@ai_router.post("/analyze")
async def analyze_content(content: str, qr_type: str):
    """Analyze QR code content for potential issues"""
    try:
        analysis = await ai_service.analyze_content(content, qr_type)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@ai_router.post("/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """Generate content based on user prompt with strict limits"""
    try:
        # Validate prompt length
        if len(request.prompt) > 2000:
            raise HTTPException(status_code=400, detail="Prompt exceeds 2000 character limit")
        
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Generate content
        result = await ai_service.generate_content_from_prompt(request.prompt, request.include_images)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "success": True,
            "content": result["content"],
            "images": result["images"],
            "token_count": result["token_count"],
            "prompt_length": result["prompt_length"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@ai_router.get("/health")
async def ai_health_check():
    """Check AI service health"""
    return {
        "status": "healthy",
        "ai_available": True,
        "service": "QuickQR AI Service (DeepSeek)",
        "provider": "DeepSeek (Free)"
    }

# Content viewing endpoints
@content_router.get("/view/{qr_id}")
async def view_content(qr_id: str, db: Session = Depends(get_db), request: Request = None):
    """View content by QR ID"""
    # Record usage for analytics
    if request:
        db_service.record_qr_usage(
            db=db,
            qr_design_id=qr_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            referrer=request.headers.get("referer")
        )
    
    content = content_service.get_content(qr_id, db)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{content.title or 'QR Content'}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .content {{ max-width: 600px; margin: 0 auto; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <div class="content">
            {f'<h1>{content.title}</h1>' if content.title else ''}
            {f'<p>{content.description}</p>' if content.description else ''}
            {f'<img src="{content.image_url}" alt="Content Image">' if content.image_url else ''}
            <div>{content.content}</div>
        </div>
    </body>
    </html>
    """)

@content_router.get("/content/{qr_id}")
async def get_content_data(qr_id: str, db: Session = Depends(get_db)):
    """Get content data by QR ID (API endpoint)"""
    content = content_service.get_content(qr_id, db)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content

@content_router.delete("/content/{qr_id}")
async def delete_content(qr_id: str, db: Session = Depends(get_db)):
    """Delete content by QR ID"""
    success = content_service.delete_content(qr_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return {"success": True, "message": "Content deleted successfully"}

# QR Design Management endpoints
@qr_router.get("/designs", response_model=List[dict])
async def get_all_designs(
    limit: int = 100, 
    offset: int = 0, 
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Get all QR designs with pagination"""
    designs = db_service.get_all_qr_designs(db, limit=limit, offset=offset)
    return [
        {
            "id": design.id,
            "title": design.title,
            "description": design.description,
            "qr_type": design.qr_type,
            "created_at": design.created_at,
            "updated_at": design.updated_at
        }
        for design in designs
    ]

@qr_router.get("/designs/{design_id}")
async def get_design(design_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Get a specific QR design by ID"""
    design = db_service.get_qr_design(db, design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return {
        "id": design.id,
        "title": design.title,
        "description": design.description,
        "content": design.content,
        "qr_type": design.qr_type,
        "size": design.size,
        "error_correction": design.error_correction,
        "border": design.border,
        "foreground_color": design.foreground_color,
        "background_color": design.background_color,
        "logo_url": design.logo_url,
        "created_at": design.created_at,
        "updated_at": design.updated_at
    }

@qr_router.put("/designs/{design_id}")
async def update_design(
    design_id: str, 
    update_data: dict, 
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Update a QR design"""
    design = db_service.update_qr_design(db, design_id, update_data)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return {"success": True, "message": "Design updated successfully"}

@qr_router.delete("/designs/{design_id}")
async def delete_design(design_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Delete a QR design"""
    success = db_service.delete_qr_design(db, design_id)
    if not success:
        raise HTTPException(status_code=404, detail="Design not found")
    
    return {"success": True, "message": "Design deleted successfully"}

@qr_router.get("/designs/{design_id}/usage")
async def get_design_usage(design_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Get usage statistics for a QR design"""
    # Check if design exists
    design = db_service.get_qr_design(db, design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    usage_stats = db_service.get_qr_usage_stats(db, design_id)
    return usage_stats

@qr_router.get("/designs/search/{query}")
async def search_designs(
    query: str, 
    limit: int = 50, 
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Search QR designs by title, description, or content"""
    designs = db_service.search_qr_designs(db, query, limit=limit)
    return [
        {
            "id": design.id,
            "title": design.title,
            "description": design.description,
            "qr_type": design.qr_type,
            "created_at": design.created_at
        }
        for design in designs
    ] 