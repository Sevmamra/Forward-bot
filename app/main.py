import logging
from telegram.ext import Application
from app.config import Config
from app.handlers import setup_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
