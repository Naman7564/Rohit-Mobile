"""
AI Product Detection Service
Supports multiple AI providers: OpenAI, Google Gemini, Anthropic Claude
"""

import json
import base64
import requests
from django.conf import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AIProductDetector:
    """Main class for AI-based product detection"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.openai_api_key = settings.OPENAI_API_KEY
        self.google_api_key = settings.GOOGLE_API_KEY
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY
    
    def detect_product_from_image(self, image_path: str) -> Optional[Dict]:
        """
        Detect product details from image
        
        Args:
            image_path: Path to the product image
            
        Returns:
            Dictionary with product details or None if detection fails
        """
        try:
            # Convert image to base64
            image_data = self._image_to_base64(image_path)
            
            if self.provider == 'openai':
                return self._detect_with_openai(image_data)
            elif self.provider == 'google':
                return self._detect_with_google(image_data)
            elif self.provider == 'anthropic':
                return self._detect_with_anthropic(image_data)
            else:
                logger.error(f"Unknown AI provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error detecting product: {str(e)}")
            return None
    
    def _image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _detect_with_openai(self, image_data: str) -> Optional[Dict]:
        """
        Detect product using OpenAI Vision API
        """
        if not self.openai_api_key:
            logger.error("OpenAI API key not configured")
            return None
        
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            prompt = """Analyze this product image and extract the following details:
            1. Product name
            2. Brand name
            3. Category (mobile, charger, cable, earbuds, accessories)
            4. Model number (if visible)
            5. Description (1-2 sentences)
            6. Color
            7. Storage variant (if applicable, e.g., 128GB, 256GB)
            
            Return ONLY a valid JSON object with these keys:
            {
                "name": "product name",
                "brand": "brand name",
                "category": "category",
                "model_number": "model number or empty string",
                "description": "product description",
                "color": "color or empty string",
                "storage_variant": "storage or empty string"
            }
            
            If you cannot determine a value, use an empty string."""
            
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ],
                    }
                ],
                max_tokens=1024,
            )
            
            # Extract and parse the JSON response
            response_text = response.choices[0].message.content
            product_data = self._parse_json_response(response_text)
            
            return product_data
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def _detect_with_google(self, image_data: str) -> Optional[Dict]:
        """
        Detect product using Google Gemini Vision API
        """
        if not self.google_api_key:
            logger.error("Google API key not configured")
            return None
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.google_api_key)
            
            model = genai.GenerativeModel('gemini-pro-vision')
            
            prompt = """Analyze this product image and extract the following details:
            1. Product name
            2. Brand name
            3. Category (mobile, charger, cable, earbuds, accessories)
            4. Model number (if visible)
            5. Description (1-2 sentences)
            6. Color
            7. Storage variant (if applicable)
            
            Return ONLY a valid JSON object with these keys:
            {
                "name": "product name",
                "brand": "brand name",
                "category": "category",
                "model_number": "model number or empty string",
                "description": "product description",
                "color": "color or empty string",
                "storage_variant": "storage or empty string"
            }"""
            
            # Convert base64 to bytes for Gemini
            import base64 as b64
            image_bytes = b64.b64decode(image_data)
            
            response = model.generate_content([
                {"mime_type": "image/jpeg", "data": image_data},
                prompt
            ])
            
            response_text = response.text
            product_data = self._parse_json_response(response_text)
            
            return product_data
            
        except Exception as e:
            logger.error(f"Google Gemini API error: {str(e)}")
            return None
    
    def _detect_with_anthropic(self, image_data: str) -> Optional[Dict]:
        """
        Detect product using Anthropic Claude Vision API
        """
        if not self.anthropic_api_key:
            logger.error("Anthropic API key not configured")
            return None
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            prompt = """Analyze this product image and extract the following details:
            1. Product name
            2. Brand name
            3. Category (mobile, charger, cable, earbuds, accessories)
            4. Model number (if visible)
            5. Description (1-2 sentences)
            6. Color
            7. Storage variant (if applicable)
            
            Return ONLY a valid JSON object with these keys:
            {
                "name": "product name",
                "brand": "brand name",
                "category": "category",
                "model_number": "model number or empty string",
                "description": "product description",
                "color": "color or empty string",
                "storage_variant": "storage or empty string"
            }"""
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            response_text = message.content[0].text
            product_data = self._parse_json_response(response_text)
            
            return product_data
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return None
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict]:
        """
        Parse JSON from API response
        """
        try:
            # Try to find JSON object in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx <= start_idx:
                logger.error("No JSON found in response")
                return None
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return None
