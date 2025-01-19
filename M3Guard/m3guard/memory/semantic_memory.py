# m3guard/memory/semantic_memory.py
from typing import Any, Dict, List, Optional
from collections import defaultdict
from .base import BaseMemory

class SemanticMemory(BaseMemory):
    """Stores learned patterns and generalizations."""
    
    def __init__(self):
        self.patterns = defaultdict(int)
        self.rules = {}
        self.violation_patterns = defaultdict(int)
        
    def store(self, data: Dict[str, Any]) -> bool:
        """Store and update patterns from interaction."""
        interaction_type = data['interaction']['type']
        outcome = data['decision']['outcome']
        
        # Update pattern frequencies
        self.patterns[interaction_type] += 1
        
        # Store violation patterns if applicable
        if not outcome['is_safe']:
            violation_key = (interaction_type, outcome['reason'])
            self.violation_patterns[violation_key] += 1
            
        # Learn new rules if clear pattern emerges
        self._update_rules()
        
        return True
        
    def retrieve(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve relevant patterns and rules."""
        interaction_type = query.get('type')
        relevant_patterns = {
            'frequency': self.patterns.get(interaction_type, 0),
            'violation_history': dict(self.violation_patterns),
            'applicable_rules': [
                rule for rule in self.rules.values()
                if self._rule_applies(rule, query)
            ]
        }
        return [relevant_patterns]
    
    def _update_rules(self):
        """Update learned rules based on observed patterns."""
        # Implement rule learning logic here
        pass
    
    def _rule_applies(self, rule: Dict, query: Dict) -> bool:
        """Check if a rule applies to the query."""
        # Implement rule matching logic here
        return True
    
    def clear(self) -> None:
        """Clear semantic memory."""
        self.patterns.clear()
        self.rules.clear()
        self.violation_patterns.clear()