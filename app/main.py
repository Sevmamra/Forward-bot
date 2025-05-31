import logging
from telegram.ext import Application
from app.config import Config
from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
