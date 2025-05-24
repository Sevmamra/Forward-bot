from telegram.ext import CommandHandler  # Corrected import
from app.config import Config
from app.bot_data import bot_data

# Rest of your commands.py code
async def start(update, context):
    if update.effective_user.id != Config.AUTHORIZED_USER_ID:
        return
    await update.message.reply_text("Bot started!")

def setup_commands(application):
    application.add_handler(CommandHandler("start", start))
