# m3guard/multimodal/image_analyzer.py
from typing import Dict, Any, Optional
from PIL import Image
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
import logging

class ImageAnalyzer:
    """Basic image content analyzer."""
    
    def __init__(self, model_name: str = "google/vit-base-patch16-224"):
        self.logger = logging.getLogger(__name__)
        try:
            self.processor = ViTImageProcessor.from_pretrained(model_name)
            self.model = ViTForImageClassification.from_pretrained(model_name)
        except Exception as e:
            self.logger.error(f"Failed to load image model: {str(e)}")
            raise
            
    async def analyze(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image content for safety issues."""
        try:
            # Process image
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get predicted class and confidence
            logits = outputs.logits
            predicted_class = logits.argmax(-1).item()
            confidence = torch.softmax(logits, dim=-1)[0][predicted_class].item()
            
            # For testing purposes, consider image safe if confidence is high
            # In production, you'd want more sophisticated safety checks
            is_safe = confidence > 0.8
            
            return {
                'is_safe': is_safe,
                'confidence': confidence,
                'predicted_class': self.model.config.id2label[predicted_class],
                'class_confidence': confidence
            }
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            return {
                'is_safe': False,
                'confidence': 1.0,
                'error': str(e)
            }