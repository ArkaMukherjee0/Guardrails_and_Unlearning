# m3guard/multimodal/guardian.py
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import logging
from .text_analyzer import TextAnalyzer
from .image_analyzer import ImageAnalyzer

class MultimodalGuardian:
    """Coordinates multimodal content analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_analyzer = TextAnalyzer()
        self.image_analyzer = ImageAnalyzer()
        
    async def analyze_content(
        self,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze multimodal content."""
        results = {
            'is_safe': True,
            'text_analysis': None,
            'image_analysis': None,
            'confidence': 1.0
        }
        
        try:
            # Analyze text if present
            if 'text' in content:
                text_results = await self.text_analyzer.analyze(content['text'])
                results['text_analysis'] = text_results
                if not text_results['is_safe']:
                    results['is_safe'] = False
                    results['confidence'] = text_results['confidence']
            
            # Analyze image if present
            if 'image' in content:
                if isinstance(content['image'], Image.Image):
                    image_results = await self.image_analyzer.analyze(content['image'])
                    results['image_analysis'] = image_results
                    if not image_results['is_safe']:
                        results['is_safe'] = False
                        results['confidence'] = max(
                            results['confidence'],
                            image_results['confidence']
                        )
            
            # Combined safety assessment
            if results['text_analysis'] and results['image_analysis']:
                results['is_safe'] = (
                    results['text_analysis']['is_safe'] and 
                    results['image_analysis']['is_safe']
                )
                
            return results
            
        except Exception as e:
            self.logger.error(f"Multimodal analysis failed: {str(e)}")
            return {
                'is_safe': False,
                'confidence': 1.0,
                'error': str(e)
            }
    
    async def check_cross_modal_consistency(
        self,
        text_results: Dict[str, Any],
        image_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check consistency between text and image content."""
        # Basic implementation - can be extended based on needs
        return {
            'is_consistent': True,
            'confidence': 1.0
        }