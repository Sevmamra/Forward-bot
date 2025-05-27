import logging
from telegram import Update
from telegram.ext import Application, ContextTypes
from app.config import Config
from app.handlers import setup_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    application = (
        Application.builder()
        .token(Config.TOKEN)
        .concurrent_updates(True)
        .build()
    )
    
    setup_handlers(application)
    logger.info("Starting bot...")
    
    try:
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == "__main__":
    run_bot()
