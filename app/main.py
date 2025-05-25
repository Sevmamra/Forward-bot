import logging
from telegram import Update
from telegram.ext import Application, ContextTypes
from app.config import Config
from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    try:
        application = (
            Application.builder()
            .token(Config.TOKEN)
            .concurrent_updates(True)
            .build()
        )
        
        setup_handlers(application)
        logger.info("Starting bot...")
        
        await application.bot.delete_webhook(drop_pending_updates=True)
        await application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False  # 🔥 Critical fix for Render
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    from asyncio import run
    run(main())  # ✅ Simplified approach that works on Render
