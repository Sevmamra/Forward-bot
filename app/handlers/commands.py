from telegram.ext import CommandHandler
from app.config import Config
from app.bot_data import bot_data

async def start(update, context):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return
    await update.message.reply_text("Bot started! Send me messages to forward.")

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
