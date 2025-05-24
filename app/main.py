from telegram.ext import Application
from config import Config
from handlers import setup_handlers

def main():
    application = Application.builder().token(Config.TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
