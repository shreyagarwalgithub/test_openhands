import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Any

from ..services.chat_service import ChatService
from ..services.research_service import ResearchService
from ..utils.config import get_config
from ..utils.html_generator import generate_update_html

class UpdateService:
    """Service for generating and sending daily updates."""
    
    def __init__(self):
        self.chat_service = ChatService()
        self.research_service = ResearchService()
        
    def generate_daily_update(self) -> Dict[str, Any]:
        """
        Generate a daily update with recent chats and research updates.
        
        Returns:
            Dictionary containing update data
        """
        # Get recent chats
        recent_chats = self.chat_service.get_recent_chats(days=1)
        
        # Extract topics from chats
        topics_by_chat = self.chat_service.extract_topics_from_chats(recent_chats)
        
        # Add topics to research service
        self.research_service.extract_topics_from_chats(topics_by_chat)
        
        # Check for updates on research topics
        topic_updates = self.research_service.check_for_updates()
        
        # Compile the update data
        update_data = {
            'timestamp': datetime.now().isoformat(),
            'chats': [chat.to_dict() for chat in recent_chats],
            'topic_updates': topic_updates,
            'all_topics': [topic.to_dict() for topic in self.research_service.get_topics()]
        }
        
        return update_data
    
    def send_email_update(self, update_data: Dict[str, Any]) -> bool:
        """
        Send an email with the daily update.
        
        Args:
            update_data: Update data to include in the email
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Get email configuration
            email_host = get_config('EMAIL_HOST')
            email_port = int(get_config('EMAIL_PORT'))
            email_user = get_config('EMAIL_USER')
            email_password = get_config('EMAIL_PASSWORD')
            email_recipient = get_config('EMAIL_RECIPIENT')
            
            # Create the email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"ChatGPT Assistant Daily Update - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = email_user
            msg['To'] = email_recipient
            
            # Generate HTML content
            html_content = generate_update_html(update_data)
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send the email
            with smtplib.SMTP(email_host, email_port) as server:
                server.starttls()
                server.login(email_user, email_password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Exception sending email update: {str(e)}")
            return False