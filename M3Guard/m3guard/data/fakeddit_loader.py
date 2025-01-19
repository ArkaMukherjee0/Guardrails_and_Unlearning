# m3guard/data/fakeddit_loader.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import pandas as pd
import logging
from pathlib import Path

@dataclass
class FakedditSample:
    text: str  # clean_title
    objects: List[str]  # Gemini objects
    label: int

class FakedditBenchmark:
    """Loader for processed Fakeddit benchmark dataset."""
    
    def __init__(self, label_type: str = "2way"):
        """
        Initialize Fakeddit benchmark loader.
        
        Args:
            label_type: One of "2way", "3way", "6way"
        """
        self.logger = logging.getLogger(__name__)
        self.label_type = label_type
        self.base_path = Path(r"C:\Users\CoolA\Code\M3Guard\m3guard\Fakeddit dataset\Processed")
        
        # Map label type to file and valid labels
        self.dataset_config = {
            "2way": {
                "file": "dataset_2way_output.txt",
                "valid_labels": [0, 1],
                "label_meanings": {
                    0: "True",
                    1: "Fake"
                }
            },
            "3way": {
                "file": "dataset_3way_output.txt",
                "valid_labels": [0, 1, 2],
                "label_meanings": {
                    0: "True",
                    1: "Fake with True Text",
                    2: "Fake with Fake Text"
                }
            },
            "6way": {
                "file": "dataset_6way.txt",
                "valid_labels": [0, 1, 2, 3, 4, 5],
                "label_meanings": {
                    0: "True",
                    1: "Satire/Parody",
                    2: "Misleading Content",
                    3: "Manipulated Content",
                    4: "False Content",
                    5: "Imposter Content"
                }
            }
        }
        
        self.data = self._load_data()
        
    def _load_data(self) -> List[FakedditSample]:
        """Load data from appropriate file based on label type."""
        samples = []
        file_path = self.base_path / self.dataset_config[self.label_type]["file"]
        valid_labels = self.dataset_config[self.label_type]["valid_labels"]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Parse [TEXT], [OBJECTS], [LABEL] format
                    # Parse the line
                    parts = line.split("[TEXT]")
                    if len(parts) != 2:
                        continue
                    after_text = parts[1]

                    text_objects_parts = after_text.split("[OBJECTS]")
                    if len(text_objects_parts) != 2:
                        continue
                    text = text_objects_parts[0].strip()
                    after_objects = text_objects_parts[1]

                    objects_label_parts = after_objects.split("[LABEL]")
                    if len(objects_label_parts) != 2:
                        continue
                    objects = objects_label_parts[0].strip()
                    label = objects_label_parts[1].strip()
                    
                    label = int(label)
                    
                    # Validate label
                    if label not in valid_labels:
                        self.logger.warning(f"Invalid label {label} found in {self.label_type} data")
                        continue
                        
                    sample = FakedditSample(
                        text=text,
                        objects=objects,
                        label=label
                    )
                    samples.append(sample)
                    
            self.logger.info(f"Loaded {len(samples)} samples for {self.label_type} classification")
            
        except Exception as e:
            self.logger.error(f"Error loading {self.label_type} data: {str(e)}")
            raise
            
        return samples
    
    def get_label_meaning(self, label: int) -> str:
        """Get human-readable meaning of a label."""
        return self.dataset_config[self.label_type]["label_meanings"].get(label, "Unknown")
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> FakedditSample:
        return self.data[idx]
    
    def get_label(self, sample: FakedditSample) -> int:
        """Get label based on specified label type."""
        return sample.label