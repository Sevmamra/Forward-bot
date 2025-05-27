import logging
from threading import Thread
from fastapi import FastAPI
import uvicorn
from telegram.ext import Application
from app.config import Config
from app.handlers import setup_handlers

# FastAPI Setup
web_app = FastAPI()
@web_app.get("/")
def health_check():
    return {"status": "Bot is running"}

def run_web():
    uvicorn.run(web_app, host="0.0.0.0", port=8000)

def run_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    Thread(target=run_web).start()
    run_bot()
