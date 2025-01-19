# m3guard/utils/vectorstore.py
from typing import Any, Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    """Simple vector store for similarity search."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.vectors = []
        self.data = []
        
    def compute_embedding(self, data: Dict[str, Any]) -> np.ndarray:
        """Compute embedding for data."""
        # Convert data to string representation for embedding
        if isinstance(data, dict):
            text = ' '.join([f"{k}: {v}" for k, v in data.items()])
        else:
            text = str(data)
            
        return self.model.encode(text)
        
    def add(self, vector: np.ndarray, data: Dict[str, Any]):
        """Add vector and associated data to store."""
        self.vectors.append(vector)
        self.data.append(data)
        
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """Find k nearest neighbors."""
        if not self.vectors:
            return []
            
        # Convert list to numpy array for efficient computation
        vectors = np.array(self.vectors)
        
        # Compute cosine similarities
        similarities = np.dot(vectors, query_vector) / (
            np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
        )
        
        # Get top k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return corresponding data
        return [self.data[i] for i in top_k_indices]
        
    def clear(self):
        """Clear all stored vectors and data."""
        self.vectors = []
        self.data = []