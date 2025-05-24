import logging
from telegram.ext import Application
from config import Config
from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Run the bot."""
    # Verify configuration
    if not Config.TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

    if Config.AUTHORIZED_USER_ID == 0:
        logger.error("❌ AUTHORIZED_USER_ID not set!")
        raise ValueError("AUTHORIZED_USER_ID not set in environment variables")

    if not Config.GROUP_IDS:
        logger.warning("⚠️ No GROUP_IDS configured - bot will only work in manually added groups")

    # Create the Application
    application = Application.builder().token(Config.TOKEN).build()

    # Setup handlers
    setup_handlers(application)

    # Run bot
    if Config.WEBHOOK_URL:
        logger.info("Starting webhook...")
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=Config.WEBHOOK_PATH,
            webhook_url=Config.WEBHOOK_URL + Config.WEBHOOK_PATH
        )
    else:
        logger.info("Starting polling...")
        application.run_polling()

if __name__ == "__main__":
    main()
