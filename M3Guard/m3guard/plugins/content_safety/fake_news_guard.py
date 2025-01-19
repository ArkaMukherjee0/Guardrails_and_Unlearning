import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if project_root not in sys.path:
   sys.path.insert(0, project_root)

from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import torch.nn.functional as F
from typing import List, Tuple, Dict, Any
import numpy as np
from m3guard.plugins.base import PluginResult, BasePlugin

class ContentAnalyzer:
    def __init__(self, model_path: str = r"C:\Users\CoolA\Code\datasets_fake_news\best_model"):
        """
        Initialize the analyzer with a fine-tuned model.
        
        Args:
            model_path: Path to the fine-tuned model
        """
        try:
            # Load tokenizer from HuggingFace hub
            self.tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
            
            # Load model from local path
            self.model = BertForSequenceClassification.from_pretrained(
                model_path,
                local_files_only=True,
                from_tf=False
            )
            self.model.eval()
            
            # Verify model loaded correctly
            if not hasattr(self.model, 'config'):
                raise ValueError("Model configuration not found")
                
            print(f"Model loaded successfully. Number of labels: {self.model.config.num_labels}")
            
        except Exception as e:
            raise RuntimeError(f"Error loading model from {model_path}: {str(e)}")

    def get_prediction(self, text: str) -> Tuple[float, torch.Tensor]:
        """
        Get misinformation prediction and hidden states for input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple containing:
                - Prediction score (0 to 1, higher means more reliable)
                - Hidden state embeddings for consistency checking
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)
            
            # Get prediction probabilities
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)
            reliable_score = probs[0][1].item()  # Assuming binary classification
            
            # Get the last hidden state for consistency checking
            hidden_states = outputs.hidden_states[-1].mean(dim=1)
            
        return reliable_score, hidden_states

class FakeNewsGuardPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.analyzer = ContentAnalyzer()
        
    @property 
    def plugin_type(self) -> str: 
        return "misinformation_guard"
        
    def _extract_text_and_objects(self, input_data: Any) -> Tuple[str, List[Dict]]:
        """
        Extract text and objects from various input formats.
        
        Args:
            input_data: Input data in various formats
            
        Returns:
            Tuple of (text, objects)
        """
        text = ""
        objects = []
        
        if isinstance(input_data, dict):
            if 'text' in input_data:
                text = str(input_data['text'])
            elif 'content' in input_data and isinstance(input_data['content'], dict):
                text = str(input_data['content'].get('text', ''))
            
            # Extract objects from various possible locations
            if 'objects' in input_data:
                objects = input_data['objects']
            elif 'content' in input_data and isinstance(input_data['content'], dict):
                objects = input_data['content'].get('objects', [])
        
        elif isinstance(input_data, str):
            text = input_data
        
        return text, objects
        
    async def check(self, 
                   user_input: Any, 
                   target_output: Dict[str, Any]) -> PluginResult:
        """
        Check if content shows signs of misinformation.
        """
        # Extract text and objects from input
        text, objects = self._extract_text_and_objects(user_input)
        
        if not text:
            return PluginResult(
                is_safe=True,
                confidence=1.0,
                reason="No text content to analyze",
                details={}
            )
        
        try:
            # Check content patterns using fine-tuned model
            reliability_score, _ = self.analyzer.get_prediction(text)
            
            # Convert reliability score to our confidence metric
            confidence = reliability_score
            
            # Determine if content is safe based on reliability score
            is_safe = reliability_score > 0.5
            
            return PluginResult(
                is_safe=is_safe,
                confidence=confidence,
                reason="Potential misinformation detected" if not is_safe else None,
                details={
                    "reliability_score": reliability_score,
                }
            )
            
        except Exception as e:
            print(f"Error in FakeNewsGuardPlugin: {str(e)}")
            # Return safe with low confidence in case of error
            return PluginResult(
                is_safe=True,
                confidence=0.1,
                reason=f"Error analyzing content: {str(e)}",
                details={}
            )