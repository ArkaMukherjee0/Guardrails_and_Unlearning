# m3guard/memory/episodic_memory.py
from typing import Any, Dict, List, Optional
import time
from .base import BaseMemory
from  ..utils.vectorstore import VectorStore

class EpisodicMemory(BaseMemory):
    """Stores specific interactions and their outcomes."""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.vector_store = VectorStore()
        self.episodes: List[Dict[str, Any]] = []
        
    def store(self, data: Dict[str, Any]) -> bool:
        """Store an interaction episode."""
        episode = {
            'timestamp': time.time(),
            'interaction': data['interaction'],
            'decision': data['decision'],
            'context': data['context'],
            'outcome': data.get('outcome', None)
        }
        
        # Store in vector database for similarity search
        embedding = self.vector_store.compute_embedding(episode)
        self.vector_store.add(embedding, episode)
        
        # Maintain fixed-size buffer
        self.episodes.append(episode)
        if len(self.episodes) > self.max_entries:
            self.episodes.pop(0)
            
        return True
        
    def retrieve(self, query: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar past episodes."""
        query_embedding = self.vector_store.compute_embedding(query)
        similar_episodes = self.vector_store.search(query_embedding, k=k)
        return similar_episodes
    
    def clear(self) -> None:
        """Clear episodic memory."""
        self.episodes.clear()
        self.vector_store.clear()