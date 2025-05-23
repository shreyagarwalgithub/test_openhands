from datetime import datetime
from typing import Dict, Any, List

def generate_update_html(update_data: Dict[str, Any]) -> str:
    """
    Generate HTML content for the daily update email.
    
    Args:
        update_data: Update data to include in the email
        
    Returns:
        HTML content as a string
    """
    timestamp = datetime.fromisoformat(update_data['timestamp']) if isinstance(update_data['timestamp'], str) else update_data['timestamp']
    chats = update_data.get('chats', [])
    topic_updates = update_data.get('topic_updates', {})
    all_topics = update_data.get('all_topics', [])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatGPT Assistant Daily Update</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            .section {{
                margin-bottom: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 20px;
            }}
            .chat-item, .topic-item, .update-item {{
                margin-bottom: 15px;
                padding: 15px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }}
            .chat-title {{
                font-weight: bold;
                color: #3498db;
            }}
            .chat-date {{
                color: #7f8c8d;
                font-size: 0.9em;
            }}
            .topic-name {{
                font-weight: bold;
                color: #2ecc71;
            }}
            .update-title {{
                font-weight: bold;
                color: #e74c3c;
            }}
            .update-link {{
                color: #3498db;
                text-decoration: none;
            }}
            .update-link:hover {{
                text-decoration: underline;
            }}
            .update-date {{
                color: #7f8c8d;
                font-size: 0.9em;
            }}
            .no-items {{
                font-style: italic;
                color: #7f8c8d;
            }}
        </style>
    </head>
    <body>
        <h1>ChatGPT Assistant Daily Update</h1>
        <p>Generated on {timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="section">
            <h2>Recent Chats</h2>
    """
    
    if chats:
        for chat in chats:
            chat_date = datetime.fromisoformat(chat['created_at']) if isinstance(chat['created_at'], str) else chat['created_at']
            html += f"""
            <div class="chat-item">
                <div class="chat-title">{chat['title']}</div>
                <div class="chat-date">{chat_date.strftime('%Y-%m-%d %H:%M:%S')}</div>
                <p>Topics: {', '.join(chat.get('topics', ['No topics extracted']))}</p>
                <p>Messages: {len(chat.get('messages', []))}</p>
            </div>
            """
    else:
        html += '<p class="no-items">No recent chats found.</p>'
    
    html += """
        </div>
        
        <div class="section">
            <h2>New Research Materials</h2>
    """
    
    if topic_updates:
        for topic_name, materials in topic_updates.items():
            html += f"""
            <div class="topic-item">
                <div class="topic-name">{topic_name}</div>
            """
            
            if materials:
                for material in materials:
                    material_date = material.get('date', 'Unknown date')
                    if isinstance(material_date, str) and material_date != 'Unknown date':
                        try:
                            material_date = datetime.fromisoformat(material_date.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                        except (ValueError, TypeError):
                            pass
                    
                    html += f"""
                    <div class="update-item">
                        <div class="update-title">{material.get('title', 'Untitled')}</div>
                        <div class="update-date">Published: {material_date}</div>
                        <p>{material.get('snippet', 'No description available')}</p>
                        <a href="{material.get('link', '#')}" class="update-link" target="_blank">Read More</a>
                    </div>
                    """
            else:
                html += '<p class="no-items">No new materials found for this topic.</p>'
                
            html += """
            </div>
            """
    else:
        html += '<p class="no-items">No new research materials found.</p>'
    
    html += """
        </div>
        
        <div class="section">
            <h2>All Tracked Research Topics</h2>
    """
    
    if all_topics:
        for topic in all_topics:
            topic_date = datetime.fromisoformat(topic['last_updated']) if isinstance(topic['last_updated'], str) else topic['last_updated']
            html += f"""
            <div class="topic-item">
                <div class="topic-name">{topic['name']}</div>
                <div class="update-date">Last checked: {topic_date.strftime('%Y-%m-%d %H:%M:%S')}</div>
                <p>Sources: {len(topic.get('sources', []))}</p>
                <p>New materials: {len(topic.get('new_materials', []))}</p>
            </div>
            """
    else:
        html += '<p class="no-items">No research topics are being tracked.</p>'
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html