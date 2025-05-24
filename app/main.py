import logging
from telegram.ext import Application
from app.config import Config
from app.handlers import setup_handlers
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Create application with unique persistence key
        application = Application.builder() \
            .token(Config.TOKEN) \
            .concurrent_updates(True) \  # Allow concurrent updates
            .build()
        
        setup_handlers(application)
        
        logger.info("Starting bot...")
        
        # Clear any pending updates
        await application.bot.delete_webhook(drop_pending_updates=True)
        
        # Start polling with clean state
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
