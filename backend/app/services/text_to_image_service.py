import os
import uuid
from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import textwrap

class TextToImageService:
    def __init__(self):
        self.images_dir = "content"
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Default font settings
        self.default_font_size = 24
        self.default_font_color = (0, 0, 0)  # Black
        self.default_bg_color = (255, 255, 255)  # White
        self.max_width = 800
        self.line_height = 30
        self.padding = 40
        
    def create_text_image(self, 
                         text: str, 
                         title: Optional[str] = None,
                         description: Optional[str] = None,
                         qr_id: str = None) -> str:
        """
        Create an image from text content and return the image path
        """
        if not qr_id:
            qr_id = str(uuid.uuid4())
            
        # Create the full content text
        full_content = ""
        if title:
            full_content += f"Title: {title}\n\n"
        if description:
            full_content += f"Description: {description}\n\n"
        full_content += text
        
        # Calculate image dimensions
        lines = textwrap.wrap(full_content, width=50)  # Wrap text to 50 characters
        text_height = len(lines) * self.line_height
        image_height = text_height + (2 * self.padding)
        
        # Create image
        image = Image.new('RGB', (self.max_width, image_height), self.default_bg_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fallback to basic if not available
        try:
            # Try to use a system font
            font = ImageFont.truetype("arial.ttf", self.default_font_size)
        except:
            try:
                # Try DejaVu Sans
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.default_font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
        
        # Draw text
        y_position = self.padding
        for line in lines:
            # Calculate text width for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.max_width - text_width) // 2
            
            draw.text((x_position, y_position), line, font=font, fill=self.default_font_color)
            y_position += self.line_height
        
        # Save image
        image_filename = f"{qr_id}_text.png"
        image_path = os.path.join(self.images_dir, image_filename)
        image.save(image_path, "PNG")
        
        return image_filename
    
    def create_styled_text_image(self, 
                                text: str, 
                                title: Optional[str] = None,
                                description: Optional[str] = None,
                                qr_id: str = None,
                                font_size: int = 24,
                                font_color: tuple = (0, 0, 0),
                                bg_color: tuple = (255, 255, 255)) -> str:
        """
        Create a styled image from text content with custom colors and font size
        """
        if not qr_id:
            qr_id = str(uuid.uuid4())
            
        # Create the full content text
        full_content = ""
        if title:
            full_content += f"Title: {title}\n\n"
        if description:
            full_content += f"Description: {description}\n\n"
        full_content += text
        
        # Calculate image dimensions
        lines = textwrap.wrap(full_content, width=50)
        text_height = len(lines) * self.line_height
        image_height = text_height + (2 * self.padding)
        
        # Create image
        image = Image.new('RGB', (self.max_width, image_height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Draw text
        y_position = self.padding
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.max_width - text_width) // 2
            
            draw.text((x_position, y_position), line, font=font, fill=font_color)
            y_position += self.line_height
        
        # Save image
        image_filename = f"{qr_id}_text.png"
        image_path = os.path.join(self.images_dir, image_filename)
        image.save(image_path, "PNG")
        
        return image_filename 