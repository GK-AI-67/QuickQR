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
    
    async def generate_content_from_prompt(self, prompt: str, include_images: bool = False) -> dict:
        """Generate content based on user prompt with strict limits using OpenAI"""
        if not self.client:
            return {"error": "AI service not available. Please set OPENAI_API_KEY."}
        if len(prompt) > 2000:
            return {"error": "Prompt exceeds 2000 character limit"}
        try:
            system_prompt = (
                "You are a content generation expert. Create engaging, informative content based on user prompts. "
                "Follow these rules: "
                "- Keep content under 20000 tokens "
                "- Use clear, professional language "
                "- Structure content with headings and paragraphs "
                "- Include relevant information and examples "
                "- Make content engaging and readable"
            )
            user_prompt = f"Generate comprehensive content based on this prompt: {prompt}"
            print(user_prompt)
        #     response = await self.client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt}
        #     ],
        #     max_tokens=2000,  # careful: 20000 is above the limit
        #     temperature=0.7
        # )

        #     print(response)
        #     generated_content = response.choices[0].message.content
        #     images = []
            import requests

            api_key = settings.GROK_API_KEY

            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 2000
            }

            response = requests.post(url, headers=headers, json=data)
            generated_content = response.json()["choices"][0]["message"]["content"]

            # print(response)
            # generated_content = response.choices[0].message.content
            images = []
            if include_images:
                images = await self._generate_images_for_content(prompt, generated_content)
            return {
                "content": generated_content,
                "images": images,
                #"token_count": response.usage.total_tokens,
                "prompt_length": len(prompt)
            }
        except Exception as e:
            return {"error": f"Content generation failed: {str(e)}"}
    
    async def _generate_images_for_content(self, prompt: str, content: str) -> List[str]:
        try:
            image_prompt = f"Create a relevant illustration for: {prompt[:100]}"
            response = await self.client.images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                size="512x512",
                quality="standard",
                n=1,
            )
            return [response.data[0].url]
        except Exception:
            return []
    
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