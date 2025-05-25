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
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    # 🔥 FIX: Use this instead of asyncio.run() for Render
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
