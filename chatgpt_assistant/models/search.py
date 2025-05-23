from datetime import datetime
from typing import List, Dict, Any

class Search:
    """Model representing a search query and its results."""
    
    def __init__(self, query: str, timestamp: datetime, results: List[Dict[str, Any]]):
        self.query = query
        self.timestamp = timestamp
        self.results = results
        self.related_topics = []  # Topics related to this search
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert search to dictionary representation."""
        return {
            'query': self.query,
            'timestamp': self.timestamp.isoformat(),
            'results': self.results,
            'related_topics': self.related_topics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Search':
        """Create a Search instance from dictionary data."""
        timestamp = datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp']
        search = cls(
            query=data['query'],
            timestamp=timestamp,
            results=data['results']
        )
        search.related_topics = data.get('related_topics', [])
        return search