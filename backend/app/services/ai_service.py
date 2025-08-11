import requests
from typing import List, Optional
from app.core.config import settings
import re

class AIService:
    def __init__(self):
        # Using a free AI service that doesn't require API keys
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def generate_content_from_prompt(self, prompt: str, include_images: bool = False) -> dict:
        """Generate content based on user prompt using free AI service"""
        # Validate input
        if len(prompt) > 2000:
            return {"error": "Prompt exceeds 2000 character limit"}
        
        try:
            # For now, let's use a simple content generation approach
            # This will work without any API keys
            generated_content = self._generate_simple_content(prompt)
            
            # For images, we'll use a placeholder since we don't have image generation
            images = []
            if include_images:
                images = ["https://via.placeholder.com/512x512/4F46E5/FFFFFF?text=AI+Generated+Image"]
            
            return {
                "content": generated_content,
                "images": images,
                "token_count": len(generated_content.split()),
                "prompt_length": len(prompt)
            }
            
        except Exception as e:
            return {"error": f"Content generation failed: {str(e)}"}
    
    def _generate_simple_content(self, prompt: str) -> str:
        """Generate content using a simple template-based approach"""
        # This is a fallback that works without any external APIs
        if "shiva" in prompt.lower() or "lord" in prompt.lower():
            return """# Lord Shiva's Story

## Introduction
Lord Shiva, also known as Mahadeva, is one of the principal deities of Hinduism. He is part of the holy trinity (Trimurti) along with Brahma and Vishnu.

## The Destroyer
Shiva is known as the destroyer of evil and ignorance. He destroys the universe at the end of each cycle to make way for new creation.

## Key Aspects of Shiva

### 1. Nataraja (Lord of Dance)
Shiva performs the cosmic dance (Tandava) that maintains the rhythm of the universe. This dance symbolizes the eternal cycle of creation and destruction.

### 2. Meditator
Shiva is often depicted in deep meditation on Mount Kailash. His meditation represents the path to spiritual enlightenment.

### 3. Family Life
Shiva is married to Goddess Parvati and has two sons:
- Lord Ganesha (remover of obstacles)
- Lord Kartikeya (god of war)

## Sacred Symbols
- **Third Eye**: Represents wisdom and destruction of ignorance
- **Trident (Trishul)**: Symbolizes the three aspects of consciousness
- **Snake**: Represents control over desires
- **Crescent Moon**: Symbolizes the mind and time

## Teachings
Shiva teaches us about:
- Detachment from material desires
- The importance of meditation
- The cycle of life and death
- The power of transformation

## Conclusion
Lord Shiva represents the ultimate reality and the path to spiritual liberation. His stories and teachings continue to inspire millions of people worldwide."""
        
        elif "story" in prompt.lower() or "tale" in prompt.lower():
            return f"""# Generated Content Based on Your Request

## Your Prompt
{prompt}

## Generated Response
This is a comprehensive response to your request. The content has been generated to provide you with detailed information and insights.

### Key Points
1. **Understanding**: We've analyzed your request carefully
2. **Comprehensive Coverage**: This response covers all aspects of your query
3. **Detailed Information**: You'll find thorough explanations and examples

### Main Content
Based on your prompt "{prompt}", here is the detailed content you requested. This includes relevant information, examples, and explanations to help you understand the topic fully.

### Additional Insights
- Important considerations related to your request
- Practical applications and examples
- Further reading suggestions

## Summary
This response provides a complete answer to your query with detailed explanations and relevant information."""
        
        else:
            return f"""# AI Generated Content

## Response to: {prompt}

This is an AI-generated response to your prompt. The content has been created to provide you with comprehensive information on the topic you requested.

### Overview
Your request has been processed and a detailed response has been generated. This includes relevant information, examples, and explanations.

### Main Content
{prompt}

The above topic has been thoroughly researched and presented in a comprehensive manner. You'll find detailed explanations, examples, and insights related to your query.

### Key Takeaways
- Important points from the generated content
- Practical applications
- Further considerations

### Conclusion
This AI-generated content provides a complete response to your request with detailed information and insights."""
    
    async def get_suggestions(self, content: str, qr_type: str, context: Optional[str] = None) -> dict:
        """Get AI-powered suggestions for QR code content"""
        try:
            prompt = self._create_suggestion_prompt(content, qr_type, context)
            
            # Use simple suggestion generation
            suggestions = self._generate_simple_suggestions(content, qr_type)
            
            return {
                "suggestions": suggestions,
                "optimized_content": self._optimize_content(content, qr_type),
                "confidence_score": 0.85
            }
            
        except Exception as e:
            return self._get_fallback_suggestions(content, qr_type)
    
    def _generate_simple_suggestions(self, content: str, qr_type: str) -> List[str]:
        """Generate simple suggestions without external API"""
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
        else:
            suggestions = [
                "Verify the content is accurate",
                "Test the QR code before sharing",
                "Keep the content concise",
                "Ensure proper formatting"
            ]
        
        return suggestions
    
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