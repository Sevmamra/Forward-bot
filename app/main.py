from telegram.ext import Application  # Make sure this is correct
from app.config import Config
from app.handlers import setup_handlers

def main():
    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
