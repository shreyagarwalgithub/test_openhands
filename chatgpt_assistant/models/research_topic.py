from datetime import datetime
from typing import List, Dict, Any

class ResearchTopic:
    """Model representing a research topic tracked by the system."""
    
    def __init__(self, name: str, last_updated: datetime, sources: List[Dict[str, Any]]):
        self.name = name
        self.last_updated = last_updated
        self.sources = sources  # List of sources (URLs, papers, etc.)
        self.new_materials = []  # New materials found since last check
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert research topic to dictionary representation."""
        return {
            'name': self.name,
            'last_updated': self.last_updated.isoformat(),
            'sources': self.sources,
            'new_materials': self.new_materials
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResearchTopic':
        """Create a ResearchTopic instance from dictionary data."""
        last_updated = datetime.fromisoformat(data['last_updated']) if isinstance(data['last_updated'], str) else data['last_updated']
        topic = cls(
            name=data['name'],
            last_updated=last_updated,
            sources=data['sources']
        )
        topic.new_materials = data.get('new_materials', [])
        return topic