from app.telegram.ext import CommandHandler
from app.config import Config

async def start(update, context):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return
    await update.message.reply_text("Bot started!")

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
