# m3guard/multimodal/text_analyzer.py
from typing import Dict, Any, Optional
from transformers import pipeline
import logging

class TextAnalyzer:
    """Basic text content analyzer."""
    
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        self.logger = logging.getLogger(__name__)
        try:
            self.classifier = pipeline("zero-shot-classification", model=model_name)
        except Exception as e:
            self.logger.error(f"Failed to load text model: {str(e)}")
            raise
            
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text content for safety issues."""
        try:
            # Define safety categories
            candidate_labels = [
                "safe content",
                "misinformation",
                "harmful content",
                "hate speech"
            ]
            
            # Classify text
            result = self.classifier(text, candidate_labels)
            
            # Determine if content is safe
            is_safe = result['labels'][0] == "safe content"
            confidence = result['scores'][0]
            
            return {
                'is_safe': is_safe,
                'confidence': confidence,
                'categories': dict(zip(result['labels'], result['scores'])),
                'text': text
            }
            
        except Exception as e:
            self.logger.error(f"Text analysis failed: {str(e)}")
            return {
                'is_safe': False,
                'confidence': 1.0,
                'error': str(e)
            }