import openai
from typing import List, Optional
from app.core.config import settings
import re

class AIService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def get_suggestions(self, content: str, qr_type: str, context: Optional[str] = None) -> dict:
        """Get AI-powered suggestions for QR code content"""
        if not self.client:
            return self._get_fallback_suggestions(content, qr_type)
        
        try:
            prompt = self._create_suggestion_prompt(content, qr_type, context)
            
            response = await self.client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a QR code optimization expert. Provide helpful suggestions for improving QR code content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            suggestions = self._parse_ai_response(response.choices[0].message.content)
            
            return {
                "suggestions": suggestions,
                "optimized_content": self._optimize_content(content, qr_type),
                "confidence_score": 0.85
            }
            
        except Exception as e:
            return self._get_fallback_suggestions(content, qr_type)
    
    def _create_suggestion_prompt(self, content: str, qr_type: str, context: Optional[str] = None) -> str:
        """Create prompt for AI suggestions"""
        base_prompt = f"""
        Analyze this QR code content and provide 3-5 specific suggestions for improvement:
        
        Content: {content}
        Type: {qr_type}
        Context: {context or 'General use'}
        
        Provide suggestions in this format:
        1. [Suggestion 1]
        2. [Suggestion 2]
        3. [Suggestion 3]
        """
        return base_prompt
    
    def _parse_ai_response(self, response: str) -> List[str]:
        """Parse AI response into list of suggestions"""
        suggestions = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and clean up
                suggestion = re.sub(r'^\d+\.\s*', '', line)
                suggestion = re.sub(r'^-\s*', '', suggestion)
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _optimize_content(self, content: str, qr_type: str) -> str:
        """Optimize content based on QR type"""
        if qr_type == "url":
            return self._optimize_url(content)
        elif qr_type == "text":
            return self._optimize_text(content)
        else:
            return content
    
    def _optimize_url(self, url: str) -> str:
        """Optimize URL for QR code"""
        # Remove trailing slashes and normalize
        url = url.strip()
        if url.endswith('/'):
            url = url[:-1]
        
        # Ensure protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url
    
    def _optimize_text(self, text: str) -> str:
        """Optimize text content"""
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        return text.strip()
    
    def _get_fallback_suggestions(self, content: str, qr_type: str) -> dict:
        """Provide fallback suggestions when AI is not available"""
        suggestions = []
        
        if qr_type == "url":
            suggestions = [
                "Ensure the URL includes https:// protocol",
                "Keep the URL short and memorable",
                "Test the URL to ensure it works correctly",
                "Consider using a URL shortener for long links"
            ]
        elif qr_type == "text":
            suggestions = [
                "Keep the text concise and clear",
                "Use proper formatting and spacing",
                "Include essential information only",
                "Consider the character limit for readability"
            ]
        elif qr_type == "contact":
            suggestions = [
                "Include full name and contact details",
                "Add company information if relevant",
                "Ensure phone numbers are properly formatted",
                "Include email address for easy contact"
            ]
        elif qr_type == "wifi":
            suggestions = [
                "Double-check the WiFi password",
                "Ensure the network name (SSID) is correct",
                "Select the appropriate encryption type",
                "Test the QR code with your device"
            ]
        else:
            suggestions = [
                "Verify the content is accurate",
                "Test the QR code before sharing",
                "Keep the content concise",
                "Ensure proper formatting"
            ]
        
        return {
            "suggestions": suggestions,
            "optimized_content": self._optimize_content(content, qr_type),
            "confidence_score": 0.6
        }
    
    async def analyze_content(self, content: str, qr_type: str) -> dict:
        """Analyze QR code content for potential issues"""
        analysis = {
            "length": len(content),
            "has_special_chars": bool(re.search(r'[^a-zA-Z0-9\s\-_\.]', content)),
            "is_url": bool(re.match(r'^https?://', content)),
            "suggestions": []
        }
        
        # Add specific analysis based on type
        if qr_type == "url":
            if not content.startswith(('http://', 'https://')):
                analysis["suggestions"].append("Consider adding https:// protocol")
            if len(content) > 100:
                analysis["suggestions"].append("URL is quite long, consider shortening")
        
        elif qr_type == "text":
            if len(content) > 200:
                analysis["suggestions"].append("Text is quite long, consider shortening")
            if not content.strip():
                analysis["suggestions"].append("Content appears to be empty")
        
        return analysis 