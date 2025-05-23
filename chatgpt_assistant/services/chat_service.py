import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests

from ..models.chat import Chat
from ..utils.config import get_config

class ChatService:
    """Service for interacting with ChatGPT API to retrieve chat history."""
    
    def __init__(self):
        self.api_key = get_config('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def get_recent_chats(self, days: int = 1) -> List[Chat]:
        """
        Retrieve recent chats from the OpenAI API.
        
        Args:
            days: Number of days to look back for chats
            
        Returns:
            List of Chat objects
        """
        # Note: This is a simplified implementation
        # The actual OpenAI API might have different endpoints/parameters
        
        since_date = datetime.now() - timedelta(days=days)
        
        try:
            # This endpoint is hypothetical and would need to be adjusted
            # based on the actual OpenAI API for retrieving chat history
            response = requests.get(
                f"{self.base_url}/conversations",
                headers=self.headers,
                params={"since": since_date.isoformat()}
            )
            
            if response.status_code == 200:
                chats_data = response.json().get("data", [])
                chats = []
                
                for chat_data in chats_data:
                    # Get detailed chat information including messages
                    chat_detail = self._get_chat_detail(chat_data["id"])
                    if chat_detail:
                        chats.append(chat_detail)
                
                return chats
            else:
                print(f"Error retrieving chats: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Exception retrieving chats: {str(e)}")
            return []
    
    def _get_chat_detail(self, chat_id: str) -> Chat:
        """
        Get detailed information for a specific chat.
        
        Args:
            chat_id: ID of the chat to retrieve
            
        Returns:
            Chat object or None if retrieval fails
        """
        try:
            # This endpoint is hypothetical
            response = requests.get(
                f"{self.base_url}/conversations/{chat_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                return Chat(
                    chat_id=data["id"],
                    title=data.get("title", "Untitled Chat"),
                    created_at=datetime.fromisoformat(data["created_at"]),
                    messages=data.get("messages", [])
                )
            else:
                print(f"Error retrieving chat detail: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception retrieving chat detail: {str(e)}")
            return None
    
    def extract_topics_from_chats(self, chats: List[Chat]) -> Dict[str, List[str]]:
        """
        Extract research topics from a list of chats.
        
        Args:
            chats: List of Chat objects
            
        Returns:
            Dictionary mapping chat IDs to lists of topics
        """
        topics_by_chat = {}
        
        for chat in chats:
            topics = chat.extract_topics()
            topics_by_chat[chat.chat_id] = topics
            chat.topics = topics
            
        return topics_by_chat