import os
from datetime import datetime
from typing import List, Dict, Any
import requests
from googleapiclient.discovery import build

from ..models.search import Search
from ..utils.config import get_config

class SearchService:
    """Service for performing searches and consolidating search results."""
    
    def __init__(self):
        self.google_api_key = get_config('GOOGLE_API_KEY')
        self.google_cse_id = get_config('GOOGLE_CSE_ID')
        
    def search_topic(self, topic: str, max_results: int = 5) -> Search:
        """
        Perform a search for a given topic.
        
        Args:
            topic: Topic to search for
            max_results: Maximum number of results to return
            
        Returns:
            Search object containing results
        """
        try:
            service = build("customsearch", "v1", developerKey=self.google_api_key)
            
            result = service.cse().list(
                q=topic,
                cx=self.google_cse_id,
                num=max_results
            ).execute()
            
            search_results = []
            for item in result.get('items', []):
                search_results.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet'),
                    'date': item.get('pagemap', {}).get('metatags', [{}])[0].get('article:published_time')
                })
            
            return Search(
                query=topic,
                timestamp=datetime.now(),
                results=search_results
            )
                
        except Exception as e:
            print(f"Exception performing search: {str(e)}")
            return Search(query=topic, timestamp=datetime.now(), results=[])
    
    def check_for_updates(self, topic: str, since_date: datetime) -> List[Dict[str, Any]]:
        """
        Check for new material on a topic since a given date.
        
        Args:
            topic: Topic to check for updates
            since_date: Date to check for updates since
            
        Returns:
            List of new materials found
        """
        try:
            # Format the date for the search query
            date_str = since_date.strftime("%Y-%m-%d")
            
            # Search with a date restriction
            service = build("customsearch", "v1", developerKey=self.google_api_key)
            
            result = service.cse().list(
                q=topic,
                cx=self.google_cse_id,
                sort="date",
                dateRestrict=f"d{(datetime.now() - since_date).days}"
            ).execute()
            
            new_materials = []
            for item in result.get('items', []):
                # Extract the date from the search result
                result_date_str = item.get('pagemap', {}).get('metatags', [{}])[0].get('article:published_time')
                
                if result_date_str:
                    try:
                        result_date = datetime.fromisoformat(result_date_str.replace('Z', '+00:00'))
                        
                        # Only include results newer than the since_date
                        if result_date > since_date:
                            new_materials.append({
                                'title': item.get('title'),
                                'link': item.get('link'),
                                'snippet': item.get('snippet'),
                                'date': result_date_str
                            })
                    except (ValueError, TypeError):
                        # If we can't parse the date, include it anyway
                        new_materials.append({
                            'title': item.get('title'),
                            'link': item.get('link'),
                            'snippet': item.get('snippet'),
                            'date': result_date_str
                        })
                else:
                    # If there's no date, include it anyway
                    new_materials.append({
                        'title': item.get('title'),
                        'link': item.get('link'),
                        'snippet': item.get('snippet'),
                        'date': None
                    })
            
            return new_materials
                
        except Exception as e:
            print(f"Exception checking for updates: {str(e)}")
            return []