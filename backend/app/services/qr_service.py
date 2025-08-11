import qrcode
from PIL import Image, ImageDraw
import base64
import io
import re
from typing import Optional
from app.models.qr_models import QRCodeRequest, ContactInfo, WiFiInfo, EmailInfo, SMSInfo

class QRCodeService:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
    
    def generate_qr_code(self, request: QRCodeRequest, qr_id: str = None, image_url: str = None) -> dict:
        """Generate QR code based on the request parameters"""
        try:
            # For content type, generate a link to the image
            if request.qr_type == "content" and qr_id:
                if image_url:
                    # Use the backend URL for the image
                    base_url = "https://quickqr-backend.onrender.com"
                    formatted_content = f"{base_url}{image_url}"
                else:
                    # Fallback to view URL
                    formatted_content = f"https://quickqr-frontend.onrender.com/view/{qr_id}"
            else:
                # Format content based on QR type
                formatted_content = self._format_content(request.content, request.qr_type)
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=self._get_error_correction(request.error_correction),
                box_size=request.size,
                border=request.border,
            )
            
            qr.add_data(formatted_content)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(
                fill_color=request.foreground_color,
                back_color=request.background_color
            )
            
            # Add logo if provided
            if request.logo_url:
                img = self._add_logo(img, request.logo_url)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "success": True,
                "qr_code_data": f"data:image/png;base64,{img_str}",
                "qr_id": qr_id,
                "view_url": f"https://quickqr-frontend.onrender.com/view/{qr_id}" if qr_id else None,
                "metadata": {
                    "content": formatted_content,
                    "qr_type": request.qr_type,
                    "size": request.size,
                    "error_correction": request.error_correction
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_content(self, content: str, qr_type: str) -> str:
        """Format content based on QR code type"""
        if qr_type == "url":
            return self._format_url(content)
        elif qr_type == "contact":
            return self._format_contact(content)
        elif qr_type == "wifi":
            return self._format_wifi(content)
        elif qr_type == "email":
            return self._format_email(content)
        elif qr_type == "phone":
            return self._format_phone(content)
        elif qr_type == "sms":
            return self._format_sms(content)
        else:
            return content
    
    def _format_url(self, url: str) -> str:
        """Format URL for QR code"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def _format_contact(self, contact_data: str) -> str:
        """Format contact information as vCard"""
        try:
            # Parse contact data (assuming JSON-like format)
            # In a real implementation, you'd parse the contact data properly
            return f"BEGIN:VCARD\nVERSION:3.0\nFN:{contact_data}\nEND:VCARD"
        except:
            return contact_data
    
    def _format_wifi(self, wifi_data: str) -> str:
        """Format WiFi credentials"""
        try:
            # Parse WiFi data
            return f"WIFI:T:WPA;S:{wifi_data};P:password;;"
        except:
            return wifi_data
    
    def _format_email(self, email_data: str) -> str:
        """Format email for QR code"""
        return f"mailto:{email_data}"
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number for QR code"""
        return f"tel:{phone}"
    
    def _format_sms(self, sms_data: str) -> str:
        """Format SMS for QR code"""
        try:
            # Parse SMS data (phone:message format)
            if ':' in sms_data:
                phone, message = sms_data.split(':', 1)
                return f"sms:{phone}:{message}"
            else:
                return f"sms:{sms_data}"
        except:
            return f"sms:{sms_data}"
    
    def _get_error_correction(self, level: str):
        """Get QR code error correction level"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        return levels.get(level, qrcode.constants.ERROR_CORRECT_M)
    
    def _add_logo(self, qr_image: Image.Image, logo_url: str) -> Image.Image:
        """Add logo to QR code (placeholder implementation)"""
        # In a real implementation, you'd download and add the logo
        return qr_image
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url)) 