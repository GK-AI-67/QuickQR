from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
from datetime import datetime

class QRCodeType(str, Enum):
    URL = "url"
    TEXT = "text"
    CONTACT = "contact"
    WIFI = "wifi"
    EMAIL = "email"
    PHONE = "phone"
    SMS = "sms"
    CONTENT = "content"  # New type for displaying content

class ErrorCorrectionLevel(str, Enum):
    L = "L"
    M = "M"
    Q = "Q"
    H = "H"

class QRCodeRequest(BaseModel):
    content: str = Field(..., description="Content for the QR code")
    qr_type: QRCodeType = Field(..., description="Type of QR code")
    size: int = Field(10, ge=1, le=40, description="QR code size")
    error_correction: ErrorCorrectionLevel = Field(ErrorCorrectionLevel.M, description="Error correction level")
    border: int = Field(4, ge=0, le=10, description="Border width")
    foreground_color: str = Field("#000000", description="Foreground color")
    background_color: str = Field("#FFFFFF", description="Background color")
    logo_url: Optional[str] = Field(None, description="Logo URL to overlay on QR code")
    title: Optional[str] = Field(None, description="Title for content display")
    description: Optional[str] = Field(None, description="Description for content display")

class QRCodeResponse(BaseModel):
    success: bool
    qr_code_data: Optional[str] = None
    qr_id: Optional[str] = None
    view_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class QRContentDisplay(BaseModel):
    qr_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    content: str
    content_type: str  # 'text', 'image', 'text+image'
    image_url: Optional[str] = None
    created_at: datetime
    qr_type: QRCodeType

class AISuggestionRequest(BaseModel):
    content: str = Field(..., description="Content to get suggestions for")
    qr_type: QRCodeType = Field(..., description="Type of QR code")
    context: Optional[str] = Field(None, description="Additional context")

class AISuggestionResponse(BaseModel):
    suggestions: List[str] = Field(..., description="List of suggestions")
    optimized_content: Optional[str] = Field(None, description="Optimized content")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score")

# Legacy models for backward compatibility
class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None

class WiFiInfo(BaseModel):
    ssid: str
    password: str
    security: str = "WPA"
    hidden: bool = False

class EmailInfo(BaseModel):
    email: str
    subject: Optional[str] = None
    body: Optional[str] = None

class SMSInfo(BaseModel):
    phone: str
    message: str 