from datetime import datetime
from typing import List, Dict, Any

class Chat:
    """Model representing a ChatGPT conversation."""
    
    def __init__(self, chat_id: str, title: str, created_at: datetime, messages: List[Dict[str, Any]]):
        self.chat_id = chat_id
        self.title = title
        self.created_at = created_at
        self.messages = messages
        self.topics = []  # Topics extracted from this chat
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert chat to dictionary representation."""
        return {
            'chat_id': self.chat_id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'messages': self.messages,
            'topics': self.topics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        """Create a Chat instance from dictionary data."""
        created_at = datetime.fromisoformat(data['created_at']) if isinstance(data['created_at'], str) else data['created_at']
        chat = cls(
            chat_id=data['chat_id'],
            title=data['title'],
            created_at=created_at,
            messages=data['messages']
        )
        chat.topics = data.get('topics', [])
        return chat
    
    def extract_topics(self) -> List[str]:
        """Extract research topics from chat content."""
        # This would use NLP or OpenAI API to extract topics
        # For now, we'll implement a simple placeholder
        topics = []
        # Implementation would analyze messages to identify key topics
        return topics