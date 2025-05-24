from telegram.ext import Application
from app.handlers import setup_handlers
from app.config import Config

def main():
    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
