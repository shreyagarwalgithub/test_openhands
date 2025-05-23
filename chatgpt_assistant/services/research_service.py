import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.research_topic import ResearchTopic
from ..services.search_service import SearchService
from ..utils.config import get_config
from ..utils.storage import save_data, load_data

class ResearchService:
    """Service for tracking research topics and checking for updates."""
    
    def __init__(self):
        self.search_service = SearchService()
        self.topics_file = "research_topics.json"
        self.topics = self._load_topics()
        
    def _load_topics(self) -> Dict[str, ResearchTopic]:
        """Load research topics from storage."""
        topics_data = load_data(self.topics_file, default=[])
        topics = {}
        
        for topic_data in topics_data:
            topic = ResearchTopic.from_dict(topic_data)
            topics[topic.name] = topic
            
        return topics
    
    def _save_topics(self):
        """Save research topics to storage."""
        topics_data = [topic.to_dict() for topic in self.topics.values()]
        save_data(self.topics_file, topics_data)
    
    def add_topic(self, name: str, sources: List[Dict[str, Any]] = None) -> ResearchTopic:
        """
        Add a new research topic to track.
        
        Args:
            name: Name of the topic
            sources: Initial sources for the topic
            
        Returns:
            The created ResearchTopic
        """
        if sources is None:
            sources = []
            
        # Check if topic already exists
        if name in self.topics:
            # Update existing topic
            topic = self.topics[name]
            # Add any new sources
            existing_urls = [s.get('link') for s in topic.sources]
            for source in sources:
                if source.get('link') not in existing_urls:
                    topic.sources.append(source)
            topic.last_updated = datetime.now()
        else:
            # Create new topic
            topic = ResearchTopic(
                name=name,
                last_updated=datetime.now(),
                sources=sources
            )
            self.topics[name] = topic
            
        self._save_topics()
        return topic
    
    def check_for_updates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Check for updates on all tracked research topics.
        
        Returns:
            Dictionary mapping topic names to lists of new materials
        """
        updates = {}
        
        for name, topic in self.topics.items():
            new_materials = self.search_service.check_for_updates(
                topic=name,
                since_date=topic.last_updated
            )
            
            if new_materials:
                topic.new_materials = new_materials
                updates[name] = new_materials
                
                # Update the last_updated timestamp
                topic.last_updated = datetime.now()
                
        self._save_topics()
        return updates
    
    def get_topics(self) -> List[ResearchTopic]:
        """Get all tracked research topics."""
        return list(self.topics.values())
    
    def extract_topics_from_chats(self, topics_by_chat: Dict[str, List[str]]):
        """
        Process topics extracted from chats.
        
        Args:
            topics_by_chat: Dictionary mapping chat IDs to lists of topics
        """
        for chat_id, topics in topics_by_chat.items():
            for topic in topics:
                # Add each topic to our tracking
                self.add_topic(name=topic)
                
        self._save_topics()