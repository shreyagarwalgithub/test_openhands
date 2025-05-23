import os
import sys
import argparse
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from chatgpt_assistant.services.update_service import UpdateService
from chatgpt_assistant.web.app import run_app
from chatgpt_assistant.utils.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def run_daily_update():
    """Run the daily update process."""
    logger.info("Running daily update...")
    
    try:
        update_service = UpdateService()
        
        # Generate the update
        update_data = update_service.generate_daily_update()
        logger.info(f"Generated update with {len(update_data.get('chats', []))} chats and {sum(len(materials) for materials in update_data.get('topic_updates', {}).values())} new materials")
        
        # Send the email
        success = update_service.send_email_update(update_data)
        
        if success:
            logger.info("Email sent successfully")
        else:
            logger.error("Failed to send email")
            
    except Exception as e:
        logger.exception(f"Error running daily update: {str(e)}")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='ChatGPT Assistant')
    parser.add_argument('--web', action='store_true', help='Run the web interface')
    parser.add_argument('--update', action='store_true', help='Run a one-time update')
    parser.add_argument('--schedule', action='store_true', help='Schedule daily updates')
    parser.add_argument('--port', type=int, default=5000, help='Port for the web interface')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host for the web interface')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    if args.update:
        # Run a one-time update
        run_daily_update()
        
    if args.schedule:
        # Schedule daily updates
        scheduler = BackgroundScheduler()
        
        # Get the update time from config
        update_time = get_config('UPDATE_TIME', '08:00')
        hour, minute = update_time.split(':')
        
        # Schedule the job
        scheduler.add_job(
            run_daily_update,
            CronTrigger(hour=int(hour), minute=int(minute)),
            id='daily_update',
            name='Daily Update',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info(f"Scheduled daily update for {update_time}")
        
    if args.web or (not args.update and not args.schedule):
        # Run the web interface
        logger.info(f"Starting web interface on {args.host}:{args.port}")
        run_app(host=args.host, port=args.port, debug=args.debug)
        
if __name__ == '__main__':
    main()